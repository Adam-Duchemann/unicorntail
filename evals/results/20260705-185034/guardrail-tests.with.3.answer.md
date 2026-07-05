```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim().toLowerCase();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  const pattern = /^(\d+(?:\.\d+)?)\s*([hms])(.*)$/;
  let remaining = trimmed;
  let totalSeconds = 0;

  while (remaining) {
    const match = remaining.match(pattern);
    if (!match) {
      throw new Error(
        `Invalid input: expected number and unit (h/m/s), got "${remaining}"`
      );
    }

    const value = parseFloat(match[1]);
    const unit = match[2];
    remaining = match[3].trim();

    if (value < 0) {
      throw new Error(`Invalid value: ${match[1]} (negative not allowed)`);
    }

    switch (unit) {
      case 'h':
        totalSeconds += value * 3600;
        break;
      case 'm':
        totalSeconds += value * 60;
        break;
      case 's':
        totalSeconds += value;
        break;
    }
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  it('parses single units', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('30m')).toBe(1800);
  });

  it('parses combined units', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('handles whitespace', () => {
    expect(parseDuration('1h 30m')).toBe(5400);
    expect(parseDuration('1 h 30 m')).toBe(5400);
    expect(parseDuration('  45s  ')).toBe(45);
  });

  it('handles decimal values', () => {
    expect(parseDuration('1.5h')).toBe(5400);
    expect(parseDuration('30.5s')).toBe(30.5);
  });

  it('case insensitive', () => {
    expect(parseDuration('1H30M')).toBe(5400);
    expect(parseDuration('45S')).toBe(45);
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('   ')).toThrow();
    expect(() => parseDuration('invalid')).toThrow();
    expect(() => parseDuration('45x')).toThrow();
    expect(() => parseDuration('h45m')).toThrow();
    expect(() => parseDuration('45m garbage')).toThrow();
  });

  it('throws on negative values', () => {
    expect(() => parseDuration('-5s')).toThrow();
  });

  it('throws on invalid input type', () => {
    expect(() => parseDuration(null as any)).toThrow();
    expect(() => parseDuration(undefined as any)).toThrow();
  });

  it('handles zero', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0h')).toBe(0);
  });

  it('accumulates repeated units', () => {
    expect(parseDuration('1h2h')).toBe(10800);
    expect(parseDuration('30s45s')).toBe(75);
  });
});
```
