"use client";

export type RunOutcome =
  | { status: "ok"; stdout: string }
  | { status: "error"; stdout: string; message: string }
  | { status: "timeout" };

type RunOptions = {
  /** Called once the Python program actually starts (after the engine has loaded). */
  onStarted?: () => void;
};

type WorkerMessage =
  | { id: number; type: "started" }
  | { id: number; type: "result"; ok: boolean; stdout: string; error: string | null };

// The first load downloads Python for the browser, which can take a while on slow connections.
const LOAD_LIMIT_MS = 60_000;

class BrowserPythonRunner {
  private worker: Worker | null = null;
  private nextId = 1;

  private ensureWorker(): Worker {
    if (!this.worker) {
      this.worker = new Worker("/pyodide-worker.js");
    }
    return this.worker;
  }

  /** Stop the worker. This is the only reliable way to halt a program stuck in a loop. */
  private reset() {
    this.worker?.terminate();
    this.worker = null;
  }

  run(code: string, stdin: string, timeLimitMs: number, options: RunOptions = {}): Promise<RunOutcome> {
    const worker = this.ensureWorker();
    const id = this.nextId++;

    return new Promise<RunOutcome>((resolve) => {
      let timer: ReturnType<typeof setTimeout> | undefined;
      let settled = false;

      const finish = (outcome: RunOutcome) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        worker.removeEventListener("message", onMessage);
        worker.removeEventListener("error", onError);
        resolve(outcome);
      };

      const onMessage = (event: MessageEvent<WorkerMessage>) => {
        const msg = event.data;
        if (msg.id !== id) return;

        if (msg.type === "started") {
          // The clock for the time limit starts now, not during the engine load.
          clearTimeout(timer);
          options.onStarted?.();
          timer = setTimeout(() => {
            this.reset();
            finish({ status: "timeout" });
          }, timeLimitMs);
          return;
        }

        if (msg.type === "result") {
          finish(
            msg.ok
              ? { status: "ok", stdout: msg.stdout }
              : { status: "error", stdout: msg.stdout, message: msg.error ?? "Unknown error" },
          );
        }
      };

      const onError = () => {
        this.reset();
        finish({ status: "error", stdout: "", message: "The Python engine stopped unexpectedly. Please try again." });
      };

      // Give up if loading takes too long, rather than waiting forever.
      timer = setTimeout(() => {
        this.reset();
        finish({
          status: "error",
          stdout: "",
          message: "Python took too long to load. Check your connection and try again.",
        });
      }, LOAD_LIMIT_MS);

      worker.addEventListener("message", onMessage);
      worker.addEventListener("error", onError);
      worker.postMessage({ id, code, stdin });
    });
  }
}

/** One shared runner for the whole page, so Python loads only once per visit. */
export const browserPython = new BrowserPythonRunner();
