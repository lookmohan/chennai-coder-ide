"use client";

import dynamic from "next/dynamic";
import { useTheme } from "next-themes";
import { useEffect, useRef, useState, type RefObject } from "react";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

// Monaco is large and browser-only, so load it on demand.
const MonacoEditor = dynamic(() => import("@monaco-editor/react").then((m) => m.default), {
  ssr: false,
  loading: () => <Skeleton className="h-full min-h-[320px] w-full" />,
});

const MONACO_LANGUAGE: Record<string, string> = {
  python: "python",
  javascript: "javascript",
  java: "java",
  cpp: "cpp",
};

/**
 * Copy, cut, paste, drag-and-drop and the right-click menu are switched off inside this editor only.
 * The listeners are attached in the capture phase on the wrapper, so they run before Monaco's own
 * handlers (which would otherwise handle the event first). This discourages copying answers. It is not
 * a security control: browser developer tools can always get around it.
 */
function useBlockClipboard(ref: RefObject<HTMLDivElement>) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const stop = (event: Event) => {
      event.preventDefault();
      event.stopPropagation();
    };

    const blockShortcuts = (event: KeyboardEvent) => {
      const modifier = event.ctrlKey || event.metaKey;
      const key = event.key.toLowerCase();
      const isClipboardShortcut =
        (modifier && (key === "c" || key === "v" || key === "x")) ||
        (event.shiftKey && key === "insert") ||
        (modifier && key === "insert");
      if (isClipboardShortcut) stop(event);
    };

    const blockedEvents = ["copy", "cut", "paste", "drop", "dragstart", "contextmenu"] as const;
    blockedEvents.forEach((name) => element.addEventListener(name, stop, true));
    element.addEventListener("keydown", blockShortcuts, true);

    return () => {
      blockedEvents.forEach((name) => element.removeEventListener(name, stop, true));
      element.removeEventListener("keydown", blockShortcuts, true);
    };
  }, [ref]);
}

export function CodeEditor({
  language,
  value,
  onChange,
  label,
  className,
}: {
  language: string;
  value: string;
  onChange: (value: string) => void;
  label: string;
  /** The parent sets the height, for example by filling a column. */
  className?: string;
}) {
  const { resolvedTheme } = useTheme();
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [fullscreen, setFullscreen] = useState(false);
  useBlockClipboard(wrapperRef);

  // Full screen: close with Escape, and stop the page behind from scrolling.
  useEffect(() => {
    if (!fullscreen) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setFullscreen(false);
    };
    // Capture phase, so Monaco cannot swallow the Escape key first.
    window.addEventListener("keydown", onKey, true);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey, true);
      document.body.style.overflow = previousOverflow;
    };
  }, [fullscreen]);

  return (
    <div
      className={cn(
        "flex flex-col gap-2",
        fullscreen && "fixed inset-0 z-50 bg-background p-3 md:p-6",
        className,
      )}
    >
      <div className="flex items-center justify-between gap-2">
        <p className="text-xs text-muted-foreground">
          {fullscreen ? "Full screen editor. Press Escape to return." : "Your Python code"}
        </p>
        <Button variant="outline" size="sm" aria-pressed={fullscreen} onClick={() => setFullscreen((f) => !f)}>
          {fullscreen ? "Exit full screen" : "Full screen"}
        </Button>
      </div>

      <div ref={wrapperRef} className="min-h-0 flex-1 overflow-hidden rounded border border-border">
        <MonacoEditor
          height="100%"
          language={MONACO_LANGUAGE[language] ?? "plaintext"}
          value={value}
          onChange={(next) => onChange(next ?? "")}
          theme={resolvedTheme === "dark" ? "vs-dark" : "light"}
          options={{
            ariaLabel: label,
            contextmenu: false,
            dropIntoEditor: { enabled: false },
            minimap: { enabled: false },
            fontSize: 14,
            tabSize: 4,
            wordWrap: "on",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            padding: { top: 12, bottom: 12 },
          }}
        />
      </div>

      <p role="note" className="text-xs text-muted-foreground">
        Type your own solution. Copy and paste are turned off in this editor, so the practice is yours.
      </p>
    </div>
  );
}
