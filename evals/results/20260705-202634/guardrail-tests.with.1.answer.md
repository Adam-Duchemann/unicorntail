No relevant prior context needed for this — it's a self-contained utility function. Here's the implementation:

```typescript
function parseDuration(input: string): number {
  const match = input.match(/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/);
  if (!match || !(match[1] || match[2] || match[3])) {
    throw new Error(`Invalid duration string: "${input}"`);
  }

  const hours = Number(match[1] ?? 0);
  const minutes = Number(match[2] ?? 0);
  const seconds = Number(match[3] ?? 0);

  return hours * 3600 + minutes * 60 + seconds;
}
```

Tests (Jest/Vitest-style — `describe`/`it`/`expect` are compatible with both):

```typescript
import { describe, it, expect } from 'vitest'; // or '@jest/globals'

describe('parseDuration', () => {
  it('parses hours, minutes, and seconds combined', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m15s')).toBe(5415);
  });

  it('parses a single unit', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('10m')).toBe(600);
  });

  it('parses zero-value units', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0h0m0s')).toBe(0);
  });

  it('parses large numbers', () => {
    expect(parseDuration('100h')).toBe(360000);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow();
  });

  it('throws on garbage input', () => {
    expect(() => parseDuration('abc')).toThrow();
    expect(() => parseDuration('1x')).toThrow();
    expect(() => parseDuration('h30m')).toThrow();
  });

  it('throws on out-of-order units', () => {
    expect(() => parseDuration('30m1h')).toThrow();
  });

  it('throws on negative numbers', () => {
    expect(() => parseDuration('-5s')).toThrow();
  });

  it('throws on whitespace or malformed separators', () => {
    expect(() => parseDuration('1h 30m')).toThrow();
    expect(() => parseDuration('1h,30m')).toThrow();
  });
});
```

Note: the regex enforces unit order (h → m → s) and rejects duplicate/out-of-order units like `30m1h` or `1h1h`.
