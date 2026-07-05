```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: expected non-empty string');
  }

  const matches = input.match(/(\d+)([hms])/g);
  if (!matches || matches.length === 0) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  // Validate that matched content accounts for the entire input (except whitespace)
  const cleanInput = input.replace(/\s/g, '');
  const matchedContent = matches.join('');
  if (matchedContent !== cleanInput) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  for (const match of matches) {
    const value = parseInt(match.slice(0, -1), 10);
    const unit = match[match.length - 1];

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
  test('parses single units', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('45s')).toBe(45);
  });

  test('parses combined units', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('2h15m30s')).toBe(8130);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('2h')).toBe(7200);
  });

  test('parses with whitespace', () => {
    expect(parseDuration('1h 30m')).toBe(5400);
    expect(parseDuration('2h 15m 30s')).toBe(8130);
  });

  test('throws on invalid format', () => {
    expect(() => parseDuration('')).toThrow('Invalid input');
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h2')).toThrow('Invalid duration format');
    expect(() => parseDuration('h1m')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h invalid')).toThrow('Invalid duration format');
  });

  test('throws on null or non-string', () => {
    expect(() => parseDuration(null as any)).toThrow();
    expect(() => parseDuration(undefined as any)).toThrow();
  });

  test('handles zero and large values', () => {
    expect(parseDuration('0h')).toBe(0);
    expect(parseDuration('100h')).toBe(360000);
    expect(parseDuration('999s')).toBe(999);
  });
});
```

The function uses a regex to extract all `number + unit` pairs, validates that the entire input is accounted for, then sums the converted values. It throws on invalid formats, non-string inputs, or unparseable content.
