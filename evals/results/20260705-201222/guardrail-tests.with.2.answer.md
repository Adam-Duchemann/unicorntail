```typescript
function parseDuration(input: string): number {
  const trimmed = input.trim();
  if (!trimmed) throw new Error('Empty duration string');

  const unitMap: { [key: string]: number } = {
    h: 3600,
    m: 60,
    s: 1,
  };

  const regex = /(\d+(?:\.\d+)?)\s*([hms])/g;
  let total = 0;
  let matched = false;
  let lastIndex = 0;

  let match;
  while ((match = regex.exec(trimmed)) !== null) {
    matched = true;
    const value = parseFloat(match[1]);
    const unit = match[2];
    total += value * unitMap[unit];
    lastIndex = match.index + match[0].length;
  }

  if (!matched || lastIndex !== trimmed.length) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  return total;
}

// Tests
describe('parseDuration', () => {
  test('parses single units', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('30m')).toBe(1800);
  });

  test('parses multiple units', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  test('handles whitespace', () => {
    expect(parseDuration('1h 30m')).toBe(5400);
    expect(parseDuration('  45s  ')).toBe(45);
  });

  test('handles decimal values', () => {
    expect(parseDuration('1.5h')).toBe(5400);
    expect(parseDuration('90.5s')).toBe(90.5);
  });

  test('throws on invalid input', () => {
    expect(() => parseDuration('')).toThrow('Empty duration string');
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h invalid')).toThrow('Invalid duration format');
  });

  test('allows any unit order', () => {
    expect(parseDuration('30m1h')).toBe(5400);
    expect(parseDuration('45s1h30m')).toBe(5445);
  });
});
```

The function uses a regex to extract all `number + unit` pairs, accumulates them with the appropriate multiplier (3600 for hours, 60 for minutes, 1 for seconds), and throws if the input is malformed or contains unexpected characters.
