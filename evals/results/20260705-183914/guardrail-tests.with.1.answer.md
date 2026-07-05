```typescript
function parseDuration(input: string): number {
  if (typeof input !== 'string') {
    throw new Error('Input must be a string');
  }

  const normalized = input.trim();
  
  if (!normalized) {
    throw new Error('Input cannot be empty');
  }

  const pattern = /(\d+)([hms])/g;
  let match;
  let total = 0;
  let lastIndex = 0;

  while ((match = pattern.exec(normalized)) !== null) {
    // Check for unexpected characters between last match and current
    if (match.index > lastIndex) {
      const between = normalized.slice(lastIndex, match.index);
      if (between.trim()) {
        throw new Error(`Invalid duration format: unexpected characters "${between}"`);
      }
    }

    const value = parseInt(match[1], 10);
    const unit = match[2];

    switch (unit) {
      case 'h':
        total += value * 3600;
        break;
      case 'm':
        total += value * 60;
        break;
      case 's':
        total += value;
        break;
    }

    lastIndex = pattern.lastIndex;
  }

  if (lastIndex === 0) {
    throw new Error('Invalid duration format: no valid duration components found');
  }

  if (lastIndex < normalized.length) {
    const remaining = normalized.slice(lastIndex);
    if (remaining.trim()) {
      throw new Error(`Invalid duration format: unexpected characters "${remaining}"`);
    }
  }

  return total;
}

// Tests
describe('parseDuration', () => {
  test('parses hours', () => {
    expect(parseDuration('2h')).toBe(7200);
  });

  test('parses minutes', () => {
    expect(parseDuration('45m')).toBe(2700);
  });

  test('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  test('parses combined units: 1h30m', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  test('parses combined units: 90m10s', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  test('parses all three units: 2h30m45s', () => {
    expect(parseDuration('2h30m45s')).toBe(9045);
  });

  test('handles whitespace at edges', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  test('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Input cannot be empty');
  });

  test('throws on non-string input', () => {
    expect(() => parseDuration(null as any)).toThrow('Input must be a string');
  });

  test('throws on no valid components', () => {
    expect(() => parseDuration('123')).toThrow('no valid duration components');
  });

  test('throws on invalid characters', () => {
    expect(() => parseDuration('1h30x')).toThrow('unexpected characters');
  });

  test('throws on spaces between units', () => {
    expect(() => parseDuration('1h 30m')).toThrow('unexpected characters');
  });

  test('handles zero values', () => {
    expect(parseDuration('0h0m0s')).toBe(0);
  });

  test('parses any unit order', () => {
    expect(parseDuration('30m5s2h')).toBe(9305);
  });
});
```

The function uses regex to find all `<number><unit>` patterns and accumulates the total seconds. It validates that all input characters are accounted for (no stray characters between or after valid components) and throws descriptive errors for invalid input.
