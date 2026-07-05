```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  const unitFactors: Record<string, number> = {
    h: 3600,
    m: 60,
    s: 1,
  };

  let totalSeconds = 0;
  const matches = trimmed.match(/(\d+)([hms])/gi);

  if (!matches || matches.length === 0) {
    throw new Error('Invalid input: no valid duration units found');
  }

  // Check for unexpected characters
  const cleanedInput = trimmed.replace(/(\d+)([hms])/gi, '').trim();
  if (cleanedInput) {
    throw new Error(`Invalid input: unexpected characters "${cleanedInput}"`);
  }

  for (const match of matches) {
    const parsed = match.match(/(\d+)([hms])/i);
    if (!parsed) continue;

    const num = parseInt(parsed[1], 10);
    const unit = parsed[2].toLowerCase();

    totalSeconds += num * unitFactors[unit];
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  test('single unit durations', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('30m')).toBe(1800);
  });

  test('multiple unit durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  test('whitespace handling', () => {
    expect(parseDuration('  1h  ')).toBe(3600);
    expect(parseDuration('1h 30m')).toBe(5400);
  });

  test('case insensitivity', () => {
    expect(parseDuration('1H30M')).toBe(5400);
    expect(parseDuration('45S')).toBe(45);
    expect(parseDuration('2H')).toBe(7200);
  });

  test('zero values', () => {
    expect(parseDuration('0h')).toBe(0);
    expect(parseDuration('0m0s')).toBe(0);
  });

  test('leading zeros', () => {
    expect(parseDuration('01h')).toBe(3600);
    expect(parseDuration('005m')).toBe(300);
  });

  test('throws on empty input', () => {
    expect(() => parseDuration('')).toThrow('empty string');
    expect(() => parseDuration('   ')).toThrow('empty string');
  });

  test('throws on no valid units', () => {
    expect(() => parseDuration('123')).toThrow('no valid duration units');
    expect(() => parseDuration('abc')).toThrow('no valid duration units');
  });

  test('throws on invalid characters', () => {
    expect(() => parseDuration('1h30m@')).toThrow('unexpected characters');
    expect(() => parseDuration('1h 30m extra')).toThrow('unexpected characters');
  });

  test('throws on non-string input', () => {
    expect(() => parseDuration(null as any)).toThrow('must be a non-empty string');
  });
});
```

The function:
- Validates input and throws on empty/invalid strings
- Matches all `\d+[hms]` patterns (case-insensitive)
- Converts each matched unit to seconds using the factor map
- Throws if any unexpected characters remain after parsing
- Handles whitespace, leading zeros, and any order of units
