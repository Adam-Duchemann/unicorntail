```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  const regex = /(\d+)([hms])/gi;
  const matches = Array.from(trimmed.matchAll(regex));

  if (matches.length === 0) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  // Verify entire input was consumed by regex
  const totalCharsMatched = matches.reduce((sum, m) => sum + m[0].length, 0);
  if (totalCharsMatched !== trimmed.length) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  const seenUnits = new Set<string>();

  for (const match of matches) {
    const value = parseInt(match[1], 10);
    const unit = match[2].toLowerCase();

    if (seenUnits.has(unit)) {
      throw new Error(`Duplicate unit "${unit}" in duration: "${input}"`);
    }
    seenUnits.add(unit);

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
  test('parses hours', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('2h')).toBe(7200);
  });

  test('parses minutes', () => {
    expect(parseDuration('1m')).toBe(60);
    expect(parseDuration('90m')).toBe(5400);
  });

  test('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('30s')).toBe(30);
  });

  test('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
    expect(parseDuration('2h10m30s')).toBe(7830);
  });

  test('handles different order of units', () => {
    expect(parseDuration('30m1h')).toBe(5400);
    expect(parseDuration('45s1h30m')).toBe(5445);
  });

  test('is case insensitive', () => {
    expect(parseDuration('1H30M')).toBe(5400);
    expect(parseDuration('45S')).toBe(45);
    expect(parseDuration('1h30M45s')).toBe(5445);
  });

  test('handles surrounding whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
    expect(parseDuration('\t2h\n')).toBe(7200);
  });

  test('throws on empty input', () => {
    expect(() => parseDuration('')).toThrow('empty string');
    expect(() => parseDuration('   ')).toThrow('empty string');
  });

  test('throws on invalid format', () => {
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('h30m')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h 30m')).toThrow('Invalid duration format');
  });

  test('throws on duplicate units', () => {
    expect(() => parseDuration('1h2h')).toThrow('Duplicate unit');
    expect(() => parseDuration('30m45m')).toThrow('Duplicate unit');
    expect(() => parseDuration('10s20s')).toThrow('Duplicate unit');
  });

  test('handles zero values', () => {
    expect(parseDuration('0h')).toBe(0);
    expect(parseDuration('0m')).toBe(0);
    expect(parseDuration('0s')).toBe(0);
  });

  test('handles large numbers', () => {
    expect(parseDuration('24h')).toBe(86400);
    expect(parseDuration('1000s')).toBe(1000);
  });
});
```

The function uses regex to extract all `<number><unit>` pairs, validates that the entire input was consumed (catching spaces and other invalid characters), checks for duplicate units, and sums the conversions. Tests cover valid formats, case-insensitivity, different orderings, edge cases, and all error conditions.
