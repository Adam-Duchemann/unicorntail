```typescript
function parseDuration(input: string): number {
  const UNITS: Record<string, number> = { h: 3600, m: 60, s: 1 };
  const ORDER = 'hms';
  const tokenPattern = /(\d+)([hms])/g;

  let totalSeconds = 0;
  let matchedLength = 0;
  let lastUnitIndex = -1;
  let match: RegExpExecArray | null;

  while ((match = tokenPattern.exec(input)) !== null) {
    const [full, amount, unit] = match;
    const unitIndex = ORDER.indexOf(unit);

    if (unitIndex <= lastUnitIndex) {
      throw new Error(`Invalid duration "${input}": units out of order or duplicated`);
    }

    lastUnitIndex = unitIndex;
    totalSeconds += Number(amount) * UNITS[unit];
    matchedLength += full.length;
  }

  if (matchedLength === 0 || matchedLength !== input.length) {
    throw new Error(`Invalid duration "${input}"`);
  }

  return totalSeconds;
}

export { parseDuration };
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

  it('parses minutes and seconds', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('parses hours, minutes, and seconds together', () => {
    expect(parseDuration('1h2m3s')).toBe(3723);
  });

  it('parses zero-valued components', () => {
    expect(parseDuration('0s')).toBe(0);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow();
  });

  it('throws on garbage input', () => {
    expect(() => parseDuration('abc')).toThrow();
  });

  it('throws on missing unit', () => {
    expect(() => parseDuration('10')).toThrow();
  });

  it('throws on unknown unit', () => {
    expect(() => parseDuration('10d')).toThrow();
  });

  it('throws on duplicate unit', () => {
    expect(() => parseDuration('1h1h')).toThrow();
  });

  it('throws on out-of-order units', () => {
    expect(() => parseDuration('30m1h')).toThrow();
  });

  it('throws on decimal values', () => {
    expect(() => parseDuration('1.5h')).toThrow();
  });

  it('throws on negative values', () => {
    expect(() => parseDuration('-5s')).toThrow();
  });

  it('throws on trailing garbage after valid tokens', () => {
    expect(() => parseDuration('1h30mx')).toThrow();
  });
});
```

Design note: units must appear in `h → m → s` order with no repeats — `"30m1h"` and `"1h1h"` both throw. If you'd rather accept any order/combination, drop the `lastUnitIndex` check and just validate full-string coverage.
