```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: expected non-empty string');
  }

  const matches = input.match(/(\d+)([hms])/g);
  if (!matches || matches.join('') !== input) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  let lastUnitIndex = -1;
  const unitOrder = { h: 0, m: 1, s: 2 };

  for (const match of matches) {
    const value = parseInt(match.slice(0, -1), 10);
    const unit = match[match.length - 1] as 'h' | 'm' | 's';
    const unitIndex = unitOrder[unit];

    if (unitIndex <= lastUnitIndex) {
      throw new Error(`Invalid duration format: units must be in order (h, m, s): "${input}"`);
    }
    lastUnitIndex = unitIndex;

    if (unit === 'h') totalSeconds += value * 3600;
    else if (unit === 'm') totalSeconds += value * 60;
    else if (unit === 's') totalSeconds += value;
  }

  return totalSeconds;
}

describe('parseDuration', () => {
  it('parses single unit durations', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses multi-unit durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('parses zero values', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0h0m0s')).toBe(0);
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('')).toThrow(/Invalid input/);
    expect(() => parseDuration('invalid')).toThrow(/Invalid duration format/);
    expect(() => parseDuration('1x')).toThrow(/Invalid duration format/);
    expect(() => parseDuration('h1m')).toThrow(/Invalid duration format/);
    expect(() => parseDuration('1h2h')).toThrow(/units must be in order/);
    expect(() => parseDuration('30s1h')).toThrow(/units must be in order/);
    expect(() => parseDuration('1h 30m')).toThrow(/Invalid duration format/);
  });

  it('throws on invalid input type', () => {
    expect(() => parseDuration(null as any)).toThrow();
    expect(() => parseDuration(123 as any)).toThrow();
  });
});
```

The function uses regex to extract all `<number><unit>` patterns, validates they cover the entire input, enforces unit ordering (h→m→s), and converts to seconds. Invalid formats, wrong unit order, and empty strings all throw errors.
