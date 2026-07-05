No prior memory on this — it's a self-contained utility task, so here's the implementation directly.

```typescript
function parseDuration(input: string): number {
  const pattern = /^(\d+h)?(\d+m)?(\d+s)?$/;
  const match = pattern.exec(input);

  if (!match || !input || match[0] === '') {
    throw new Error(`Invalid duration string: "${input}"`);
  }

  const [, hours, minutes, seconds] = match;
  if (!hours && !minutes && !seconds) {
    throw new Error(`Invalid duration string: "${input}"`);
  }

  const h = hours ? parseInt(hours, 10) : 0;
  const m = minutes ? parseInt(minutes, 10) : 0;
  const s = seconds ? parseInt(seconds, 10) : 0;

  return h * 3600 + m * 60 + s;
}
```

```typescript
import { describe, it, expect } from 'vitest'; // swap for jest's globals if needed
import { parseDuration } from './parseDuration';

describe('parseDuration', () => {
  it('parses hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(90 * 60);
  });

  it('parses seconds only', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses hours only', () => {
    expect(parseDuration('2h')).toBe(2 * 3600);
  });

  it('parses minutes and seconds', () => {
    expect(parseDuration('90m10s')).toBe(90 * 60 + 10);
  });

  it('parses all three units', () => {
    expect(parseDuration('1h2m3s')).toBe(3600 + 2 * 60 + 3);
  });

  it('parses zero values', () => {
    expect(parseDuration('0h0m0s')).toBe(0);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow();
  });

  it('throws on garbage input', () => {
    expect(() => parseDuration('abc')).toThrow();
  });

  it('throws on wrong unit order', () => {
    expect(() => parseDuration('30m1h')).toThrow();
  });

  it('throws on missing unit suffix', () => {
    expect(() => parseDuration('90')).toThrow();
  });

  it('throws on duplicate units', () => {
    expect(() => parseDuration('1h1h')).toThrow();
  });

  it('throws on negative numbers', () => {
    expect(() => parseDuration('-5s')).toThrow();
  });
});
```

Note: units must appear in `h`, `m`, `s` order (each optional, no duplicates) — `1h30m` and `90m10s` both fit this; `30m1h` is rejected as out-of-order. Adjust the regex if you need order-independent parsing.
