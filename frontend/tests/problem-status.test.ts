import { describe, expect, it } from "vitest";

import { difficultyStage, isFinal, STATUS_COPY } from "@/features/problems/status";
import type { SubmissionStatus } from "@/features/problems/types";

describe("isFinal (controls when results polling stops)", () => {
  it("keeps polling while the judge is still working", () => {
    expect(isFinal("QUEUED")).toBe(false);
    expect(isFinal("RUNNING")).toBe(false);
  });

  it("stops polling once there is a verdict", () => {
    expect(isFinal("ACCEPTED")).toBe(true);
    expect(isFinal("WRONG_ANSWER")).toBe(true);
    expect(isFinal("SYSTEM_ERROR")).toBe(true);
  });

  it("does not treat a missing status as final", () => {
    expect(isFinal(undefined)).toBe(false);
    expect(isFinal(null)).toBe(false);
  });
});

describe("STATUS_COPY", () => {
  const every: SubmissionStatus[] = [
    "QUEUED",
    "RUNNING",
    "ACCEPTED",
    "WRONG_ANSWER",
    "COMPILATION_ERROR",
    "RUNTIME_ERROR",
    "TIME_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "SYSTEM_ERROR",
  ];

  it("has friendly copy for every status the backend can return", () => {
    for (const status of every) {
      expect(STATUS_COPY[status].label.length).toBeGreaterThan(0);
      expect(STATUS_COPY[status].encouragement.length).toBeGreaterThan(20);
    }
  });

  it("never blames the student for a system error", () => {
    expect(STATUS_COPY.SYSTEM_ERROR.encouragement.toLowerCase()).toContain("our side");
  });

  it("celebrates an accepted solution", () => {
    expect(STATUS_COPY.ACCEPTED.label).toBe("Accepted");
  });
});

describe("difficultyStage", () => {
  it("gives each level a learning stage name", () => {
    expect(difficultyStage("Easy")).toBe("Warm-up");
    expect(difficultyStage("Medium")).toBe("Building blocks");
    expect(difficultyStage("Hard")).toBe("Level up");
  });
});
