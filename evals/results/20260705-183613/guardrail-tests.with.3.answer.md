```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim().toLowerCase();
  
  // Validate format: must have at least one unit with a value
  const regex = /^(\d+(?:\.\d+)?[hms])+$/;
  if (!regex.test(trimmed)) {
    throw new Error(`Invalid duration format: "${input}". Expected format like "1h30m45s" or "45s"`);
  }

  let totalSeconds = 0;
  const units = trimmed.match(/(\d+(?:\.\d+)?)([hms])/g);
  const seen = new Set<string>();

  for (const unit of units!) {
    const match = unit.match(/(\d+(?:\.\d+)?)([hms])/);
    const value = parseFloat(match![1]);
    const type = match![2];

    if (seen.has(type)) {
      throw new Error(`Duplicate unit "${type}" in duration string`);
    }
    seen.add(type);

    totalSeconds += type === 'h' ? value * 3600 : type === 'm' ? value * 60 : value;
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  test('parses single units', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2m')).toBe(120);
    expect(parseDuration('1h')).toBe(3600);
  });

  test('parses combined units in order', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('2h45m30s')).toBe(9930);
    expect(parseDuration('90m10s')).toBe(5410);
  });

  test('parses unordered units', () => {
    expect(parseDuration('30s45m1h')).toBe(5475);
    expect(parseDuration('45m30s2h')).toBe(9870);
  });

  test('parses decimal values', () => {
    expect(parseDuration('1.5h')).toBe(5400);
    expect(parseDuration('90.5m')).toBe(5430);
  });

  test('handles whitespace and case insensitivity', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
    expect(parseDuration('1H30M45S')).toBe(5445);
  });

  test('throws on empty or invalid input', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('   ')).toThrow();
    expect(() => parseDuration('invalid')).toThrow();
  });

  test('throws on invalid format', () => {
    expect(() => parseDuration('45')).toThrow();
    expect(() => parseDuration('1x30m')).toThrow();
    expect(() => parseDuration('h30m')).toThrow();
  });

  test('throws on duplicate units', () => {
    expect(() => parseDuration('1h30m15m')).toThrow();
    expect(() => parseDuration('45s30s')).toThrow();
  });
});
```

The function:
- Validates input format with regex
- Extracts value-unit pairs (h/m/s)
- Detects duplicates and invalid formats
- Returns total seconds as a number
- Throws with descriptive errors on any invalid input
