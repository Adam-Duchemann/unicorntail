```typescript
function parseDuration(input: string): number {
  if (typeof input !== 'string') {
    throw new Error('Invalid duration: input must be a string');
  }

  const trimmed = input.trim().toLowerCase();
  
  if (trimmed === '') {
    throw new Error('Invalid duration: input cannot be empty');
  }

  // Validate format: pattern like "1h30m45s"
  const regex = /^(\d+h)?(\d+m)?(\d+s)?$/;
  
  if (!regex.test(trimmed)) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  
  const hoursMatch = trimmed.match(/(\d+)h/);
  if (hoursMatch) {
    totalSeconds += parseInt(hoursMatch[1], 10) * 3600;
  }

  const minutesMatch = trimmed.match(/(\d+)m/);
  if (minutesMatch) {
    totalSeconds += parseInt(minutesMatch[1], 10) * 60;
  }

  const secondsMatch = trimmed.match(/(\d+)s/);
  if (secondsMatch) {
    totalSeconds += parseInt(secondsMatch[1], 10);
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  it('parses single units', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('1h30m45s')).toBe(5445);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('2h')).toBe(7200);
  });

  it('is case-insensitive', () => {
    expect(parseDuration('1H')).toBe(3600);
    expect(parseDuration('1H30M45S')).toBe(5445);
  });

  it('trims whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('throws on empty input', () => {
    expect(() => parseDuration('')).toThrow('input cannot be empty');
    expect(() => parseDuration('   ')).toThrow('input cannot be empty');
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('h1m')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h 30m')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h30m45')).toThrow('Invalid duration format');
    expect(() => parseDuration('1.5h')).toThrow('Invalid duration format');
  });

  it('throws on non-string input', () => {
    expect(() => parseDuration(123 as any)).toThrow('must be a string');
  });

  it('handles zero values', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0h0m0s')).toBe(0);
  });
});
```
