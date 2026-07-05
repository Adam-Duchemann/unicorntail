```typescript
function parseDuration(input: string): number {
  if (typeof input !== 'string' || !input.trim()) {
    throw new Error('Invalid duration: input must be a non-empty string');
  }

  const normalized = input.trim().toLowerCase();
  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = normalized.match(pattern);

  if (!match) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseInt(match[3], 10) : 0;

  if (hours === 0 && minutes === 0 && seconds === 0) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  return hours * 3600 + minutes * 60 + seconds;
}

// Tests
describe('parseDuration', () => {
  it('parses hours', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses minutes', () => {
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('90m')).toBe(5400);
  });

  it('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('120s')).toBe(120);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('1h30m45s')).toBe(5445);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('2h')).toBe(7200);
  });

  it('handles case-insensitive input', () => {
    expect(parseDuration('1H30M')).toBe(5400);
    expect(parseDuration('45S')).toBe(45);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('   ')).toThrow();
    expect(() => parseDuration('1x')).toThrow();
    expect(() => parseDuration('m30')).toThrow();
    expect(() => parseDuration('1h 30m')).toThrow();
    expect(() => parseDuration('abc')).toThrow();
    expect(() => parseDuration('0h0m0s')).toThrow();
  });
});
```

The function:
- Parses `h` (hours), `m` (minutes), `s` (seconds) in any order
- Converts to total seconds (hours × 3600 + minutes × 60 + seconds)
- Handles case-insensitive input and whitespace
- Throws on invalid formats, missing units, or all-zero durations
