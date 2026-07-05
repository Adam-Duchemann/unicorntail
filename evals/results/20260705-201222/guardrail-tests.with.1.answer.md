```typescript
// Function
function parseDuration(input: string): number {
  if (typeof input !== 'string' || !input.trim()) {
    throw new Error('Invalid input: duration must be a non-empty string');
  }

  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = input.trim().match(pattern);

  if (!match || !match[0]) {
    throw new Error(
      `Invalid duration format: "${input}". Expected format like "1h30m", "45s", "2h", "90m10s"`
    );
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseInt(match[3], 10) : 0;

  return hours * 3600 + minutes * 60 + seconds;
}

// Tests
describe('parseDuration', () => {
  it('parses single units', () => {
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('throws on empty or invalid formats', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('   ')).toThrow();
    expect(() => parseDuration('1x')).toThrow();
    expect(() => parseDuration('30m1h')).toThrow();
    expect(() => parseDuration('1h2h')).toThrow();
    expect(() => parseDuration('invalid')).toThrow();
  });
});
```

The regex enforces strict ordering (hours → minutes → seconds) and rejects duplicates or malformed input. Each test case covers a valid pattern, whitespace handling, and common error cases.
