No prior memory on this, so I'll go straight to the answer.

```typescript
function parseDuration(input: string): number {
  const pattern = /^(\d+h)?(\d+m)?(\d+s)?$/;
  const match = pattern.exec(input);
  if (!match || !input) {
    throw new Error(`Invalid duration: "${input}"`);
  }
  const [, h, m, s] = match;
  if (!h && !m && !s) {
    throw new Error(`Invalid duration: "${input}"`);
  }

  const hours = h ? parseInt(h, 10) : 0;
  const minutes = m ? parseInt(m, 10) : 0;
  const seconds = s ? parseInt(s, 10) : 0;

  return hours * 3600 + minutes * 60 + seconds;
}

export { parseDuration };
```

```typescript
import { describe, it, expect } from "vitest"; // or from "@jest/globals"
import { parseDuration } from "./parseDuration";

describe("parseDuration", () => {
  it("parses hours and minutes", () => {
    expect(parseDuration("1h30m")).toBe(90 * 60);
  });

  it("parses seconds only", () => {
    expect(parseDuration("45s")).toBe(45);
  });

  it("parses hours only", () => {
    expect(parseDuration("2h")).toBe(2 * 3600);
  });

  it("parses minutes and seconds", () => {
    expect(parseDuration("90m10s")).toBe(90 * 60 + 10);
  });

  it("parses hours, minutes, and seconds together", () => {
    expect(parseDuration("1h2m3s")).toBe(3600 + 120 + 3);
  });

  it("parses minutes only", () => {
    expect(parseDuration("5m")).toBe(5 * 60);
  });

  it("parses zero values", () => {
    expect(parseDuration("0h0m0s")).toBe(0);
  });

  it("throws on empty string", () => {
    expect(() => parseDuration("")).toThrow();
  });

  it("throws on garbage input", () => {
    expect(() => parseDuration("abc")).toThrow();
  });

  it("throws on wrong unit order", () => {
    expect(() => parseDuration("30m1h")).toThrow();
  });

  it("throws on missing unit suffix", () => {
    expect(() => parseDuration("30")).toThrow();
  });

  it("throws on duplicate units", () => {
    expect(() => parseDuration("1h1h")).toThrow();
  });

  it("throws on negative numbers", () => {
    expect(() => parseDuration("-5m")).toThrow();
  });

  it("throws on decimal values", () => {
    expect(() => parseDuration("1.5h")).toThrow();
  });
});
```

Note: units must appear in `h`, `m`, `s` order (matching your examples); mixed order like `"30m1h"` is rejected. Say so if you want order-independent parsing instead.
