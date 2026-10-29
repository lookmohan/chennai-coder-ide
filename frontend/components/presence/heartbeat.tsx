"use client";

import { useEffect } from "react";

import { api } from "@/lib/api";

const EVERY_MINUTE = 60_000;

/**
 * Quietly tells the server this person is here, once a minute, so others see them as Online.
 * Renders nothing. Runs for as long as the signed-in app is open.
 */
export function Heartbeat() {
  useEffect(() => {
    const ping = () => {
      if (document.visibilityState === "visible") {
        void api("/users/me").catch(() => undefined);
      }
    };
    ping();
    const timer = window.setInterval(ping, EVERY_MINUTE);
    return () => window.clearInterval(timer);
  }, []);
  return null;
}
