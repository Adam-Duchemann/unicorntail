No prior memory on this — proceeding directly.

```typescript
function parseDuration(input: string): number {
  const match = input.match(/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/);
  if (!match || !input) {
    throw new Error(`Invalid duration string: "${input}"`);
  }

  const [, hours, minutes, seconds] = match;
  if (!hours && !minutes && !seconds) {
    throw new Error(`Invalid duration string: "${input}"`);
  }

  return (
    Number(hours ?? 0) * 3600 +
    Number(minutes ?? 0) * 60 +
    Number(seconds ?? 0)
  );
}
```

```typescript
import { describe, it, expect } from "vitest"; // or "@jest/globals"
import { parseDuration } from "./parseDuration";

describe("parseDuration", () => {
  it("parses hours and minutes", () => {
    expect(parseDuration("1h30m")).toBe(5400);
  });

  it("parses seconds only", () => {
    expect(parseDuration("45s")).toBe(45);
  });

  it("parses hours only", () => {
    expect(parseDuration("2h")).toBe(7200);
  });

  it("parses minutes and seconds", () => {
    expect(parseDuration("90m10s")).toBe(5410);
  });

  it("parses hours, minutes, and seconds together", () => {
    expect(parseDuration("1h2m3s")).toBe(3723);
  });

  it("parses a single unit with multiple digits", () => {
    expect(parseDuration("100s")).toBe(100);
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
    expect(() => parseDuration("90")).toThrow();
  });

  it("throws on negative numbers", () => {
    expect(() => parseDuration("-5s")).toThrow();
  });
});
```
