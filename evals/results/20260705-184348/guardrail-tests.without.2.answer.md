```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid duration: cannot be empty');
  }

  // Pattern: optional hours, optional minutes, optional seconds (in that order)
  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = trimmed.match(pattern);

  if (!match) {
    throw new Error(
      `Invalid duration format: "${input}". Expected format like "1h30m", "45s", "2h", etc.`
    );
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseInt(match[3], 10) : 0;

  // At least one unit must be present
  if (hours === 0 && minutes === 0 && seconds === 0) {
    throw new Error(
      `Invalid duration: "${input}". Must include at least one time unit (h, m, or s)`
    );
  }

  return hours * 3600 + minutes * 60 + seconds;
}

// Tests
describe('parseDuration', () => {
  it('parses single units', () => {
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('45m')).toBe(2700);
    expect(parseDuration('30s')).toBe(30);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('1h30m45s')).toBe(5445);
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  2h  ')).toBe(7200);
    expect(parseDuration('\t45s\n')).toBe(45);
  });

  it('allows zero values in mixed units', () => {
    expect(parseDuration('1h0m30s')).toBe(3630);
    expect(parseDuration('0h45m')).toBe(2700);
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('invalid')).toThrow();
    expect(() => parseDuration('1x')).toThrow();
    expect(() => parseDuration('30m1h')).toThrow(); // wrong order
    expect(() => parseDuration('1h 30m')).toThrow(); // space between units
  });

  it('throws on empty or whitespace-only input', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('   ')).toThrow();
  });

  it('throws on zero-only duration', () => {
    expect(() => parseDuration('0h')).toThrow();
    expect(() => parseDuration('0h0m0s')).toThrow();
  });

  it('handles large values', () => {
    expect(parseDuration('24h')).toBe(86400);
    expect(parseDuration('1000h')).toBe(3600000);
  });
});
```
