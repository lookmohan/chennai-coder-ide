import { beforeEach, describe, expect, it } from "vitest";

import { markSolved, readSolved } from "@/features/progress/solved";

describe("solved problems (browser storage, per account)", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("starts empty for a new account", () => {
    expect(readSolved("user-a")).toEqual({});
  });

  it("marks a problem solved the first time only", () => {
    expect(markSolved("user-a", "say-hello")).toBe(true);
    expect(markSolved("user-a", "say-hello")).toBe(false);
    expect(Object.keys(readSolved("user-a"))).toEqual(["say-hello"]);
  });

  it("keeps accounts separate in the same browser", () => {
    markSolved("admin-id", "say-hello");
    expect(readSolved("student-id")).toEqual({});
    expect(readSolved("admin-id")).toHaveProperty("say-hello");
  });

  it("recovers from corrupted saved data instead of breaking the page", () => {
    window.localStorage.setItem("cc-solved-problems:user-a", "{not json");
    expect(readSolved("user-a")).toEqual({});
    expect(markSolved("user-a", "is-even")).toBe(true);
  });

  it("ignores saved data that is not an object", () => {
    window.localStorage.setItem("cc-solved-problems:user-a", "[1,2,3]");
    expect(readSolved("user-a")).toEqual({});
  });
});
