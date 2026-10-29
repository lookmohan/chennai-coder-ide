// Runs Python in a background thread, so a slow or endless program can be stopped.
// This is a classic worker loaded from /public, using importScripts, which keeps setup simple.
// Pyodide is a free, open-source Python for the browser. It is downloaded from a public CDN.

const PYODIDE_VERSION = "0.26.4";
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

let enginePromise = null;

function loadEngine() {
  if (!enginePromise) {
    enginePromise = (async () => {
      importScripts(`${PYODIDE_BASE}pyodide.js`);
      return await loadPyodide({ indexURL: PYODIDE_BASE });
    })();
    // If loading fails, allow a retry on the next run.
    enginePromise.catch(() => {
      enginePromise = null;
    });
  }
  return enginePromise;
}

// Turn the example input into the lines input() should read, without the final newline.
function splitLines(stdin) {
  if (!stdin) return [];
  const trimmed = stdin.endsWith("\n") ? stdin.slice(0, -1) : stdin;
  return trimmed.split("\n");
}

self.onmessage = async (event) => {
  const { id, code, stdin } = event.data;

  let py;
  try {
    py = await loadEngine();
  } catch (err) {
    self.postMessage({
      id,
      type: "result",
      ok: false,
      stdout: "",
      error: "Could not load the Python engine. Check your internet connection and try again.",
    });
    return;
  }

  // Tell the page the program is about to run, so the time limit starts now (not during loading).
  self.postMessage({ id, type: "started" });

  const lines = splitLines(stdin);
  const output = [];
  py.setStdin({ stdin: () => (lines.length ? lines.shift() : undefined) });
  py.setStdout({ batched: (text) => output.push(text) });

  const stdoutSoFar = () => output.join("\n") + (output.length ? "\n" : "");

  try {
    // A fresh namespace for every run, so one test cannot leak variables into the next.
    const namespace = py.globals.get("dict")();
    py.runPython(code, { globals: namespace });
    namespace.destroy();
    self.postMessage({ id, type: "result", ok: true, stdout: stdoutSoFar(), error: null });
  } catch (err) {
    self.postMessage({
      id,
      type: "result",
      ok: false,
      stdout: stdoutSoFar(),
      error: String(err && err.message ? err.message : err),
    });
  }
};
