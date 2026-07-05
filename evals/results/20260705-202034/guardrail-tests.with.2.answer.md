```typescript
export function parseDuration(input: string): number {
  const match = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/.exec(input);
  if (!match || (!match[1] && !match[2] && !match[3])) {
    throw new Error(`Invalid duration: "${input}"`);
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseInt(match[3], 10) : 0;

  return hours * 3600 + minutes * 60 + seconds;
}
```

```typescript
import { parseDuration } from './parseDuration';

describe('parseDuration', () => {
  it('parses hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  it('parses seconds only', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses hours only', () => {
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses minutes and seconds with values over 59', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('parses hours, minutes, and seconds together', () => {
    expect(parseDuration('1h2m3s')).toBe(3723);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow();
  });

  it('throws on garbage input', () => {
    expect(() => parseDuration('abc')).toThrow();
  });

  it('throws on out-of-order units', () => {
    expect(() => parseDuration('30m1h')).toThrow();
  });

  it('throws on duplicate units', () => {
    expect(() => parseDuration('1h1h')).toThrow();
  });

  it('throws on negative numbers', () => {
    expect(() => parseDuration('-5s')).toThrow();
  });

  it('throws on decimal numbers', () => {
    expect(() => parseDuration('1.5h')).toThrow();
  });

  it('throws on unknown unit', () => {
    expect(() => parseDuration('5d')).toThrow();
  });
});
```

Units must appear in `h` → `m` → `s` order with no duplicates or extra characters; anything else (empty, decimals, negatives, unknown units, wrong order) throws.
