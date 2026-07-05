```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = input.match(pattern);

  if (!match || (match[1] === undefined && match[2] === undefined && match[3] === undefined)) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let seconds = 0;

  if (match[1]) seconds += parseInt(match[1], 10) * 3600;
  if (match[2]) seconds += parseInt(match[2], 10) * 60;
  if (match[3]) seconds += parseInt(match[3], 10);

  return seconds;
}

// Tests
describe('parseDuration', () => {
  test('parses hours', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('2h')).toBe(7200);
  });

  test('parses minutes', () => {
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('45m')).toBe(2700);
  });

  test('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('90s')).toBe(90);
  });

  test('parses combinations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('2h15m30s')).toBe(8130);
    expect(parseDuration('90m10s')).toBe(5410);
  });

  test('parses zero values', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0m0s')).toBe(0);
  });

  test('throws on invalid format', () => {
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h30x')).toThrow('Invalid duration format');
    expect(() => parseDuration('h30m')).toThrow('Invalid duration format');
    expect(() => parseDuration('1 h')).toThrow('Invalid duration format');
    expect(() => parseDuration('m10s')).toThrow('Invalid duration format');
  });

  test('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Invalid duration format');
  });

  test('throws on no components', () => {
    expect(() => parseDuration('xyz')).toThrow('Invalid duration format');
  });
});
```

The function:
- Uses regex `/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/` to enforce valid format with units in order (h→m→s)
- Extracts each component and multiplies by the appropriate factor (3600 for hours, 60 for minutes, 1 for seconds)
- Throws if input is empty, not a string, invalid format, or has no components
- Handles all your examples: "1h30m" → 5400, "45s" → 45, "2h" → 7200, "90m10s" → 5410
