```typescript
function parseDuration(input: string): number {
  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = input.match(pattern);

  if (!match) {
    throw new Error(`Invalid duration format: ${input}`);
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseInt(match[3], 10) : 0;

  if (hours === 0 && minutes === 0 && seconds === 0) {
    throw new Error(`Invalid duration format: ${input}`);
  }

  return hours * 3600 + minutes * 60 + seconds;
}

describe('parseDuration', () => {
  it('parses hours', () => {
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses minutes', () => {
    expect(parseDuration('30m')).toBe(1800);
  });

  it('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  it('parses minutes and seconds', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('parses hours, minutes, and seconds', () => {
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Invalid duration format');
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
  });

  it('throws on invalid units', () => {
    expect(() => parseDuration('1d')).toThrow('Invalid duration format');
  });

  it('throws on wrong unit order', () => {
    expect(() => parseDuration('30m1h')).toThrow('Invalid duration format');
  });

  it('throws on zero duration', () => {
    expect(() => parseDuration('0h')).toThrow('Invalid duration format');
  });

  it('allows zero in non-zero duration', () => {
    expect(parseDuration('0h30m')).toBe(1800);
  });
});
```
