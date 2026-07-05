```typescript
function parseDuration(input: string): number {
  if (typeof input !== 'string' || input.length === 0) {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const units: Record<string, number> = { h: 3600, m: 60, s: 1 };
  let total = 0;
  let consumed = 0;

  const regex = /(\d+)([hms])/g;
  let match;
  
  while ((match = regex.exec(input)) !== null) {
    if (match.index !== consumed) {
      throw new Error(`Invalid input: unexpected characters "${input.slice(consumed, match.index)}"`);
    }
    total += parseInt(match[1], 10) * units[match[2]];
    consumed = regex.lastIndex;
  }

  if (consumed === 0) {
    throw new Error('Invalid input: no valid duration units found');
  }

  if (consumed !== input.length) {
    throw new Error(`Invalid input: unexpected characters "${input.slice(consumed)}"`);
  }

  return total;
}

// Tests
describe('parseDuration', () => {
  test('parses single hour', () => {
    expect(parseDuration('2h')).toBe(7200);
  });

  test('parses single minute', () => {
    expect(parseDuration('45m')).toBe(2700);
  });

  test('parses single second', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  test('parses combined hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  test('parses all three units', () => {
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  test('parses hours and seconds', () => {
    expect(parseDuration('2h10s')).toBe(7210);
  });

  test('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('no valid duration units');
  });

  test('throws on non-string input', () => {
    expect(() => parseDuration(null as any)).toThrow();
  });

  test('throws on string with no units', () => {
    expect(() => parseDuration('123')).toThrow('no valid duration units');
  });

  test('throws on invalid unit', () => {
    expect(() => parseDuration('1d')).toThrow('no valid duration units');
  });

  test('throws on unit before number', () => {
    expect(() => parseDuration('h1m2')).toThrow('unexpected characters');
  });

  test('throws on invalid characters (spaces)', () => {
    expect(() => parseDuration('1h 30m')).toThrow('unexpected characters');
  });

  test('handles zero values', () => {
    expect(parseDuration('0h')).toBe(0);
  });

  test('parses large values', () => {
    expect(parseDuration('100h50m30s')).toBe(362430);
  });
});
```

**Logic:** regex captures number + unit pairs sequentially. Tracks consumed positions to catch gaps (invalid chars) and ensures entire string is parsed. Units map to seconds: h=3600, m=60, s=1.
