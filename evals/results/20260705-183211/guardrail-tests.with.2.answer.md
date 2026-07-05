```typescript
function parseDuration(input: string): number {
  if (typeof input !== 'string') {
    throw new Error('Invalid input: not a string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Empty duration string');
  }

  // Pattern: hours, minutes, seconds in that order, each optional
  const pattern = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
  const match = trimmed.match(pattern);

  if (!match) {
    throw new Error(`Invalid duration format: ${input}`);
  }

  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const secs = match[3] ? parseInt(match[3], 10) : 0;

  // Ensure at least one unit is present
  if (hours === 0 && minutes === 0 && secs === 0) {
    throw new Error(`Invalid duration format: ${input}`);
  }

  return hours * 3600 + minutes * 60 + secs;
}

// Tests
describe('parseDuration', () => {
  it('parses hours', () => {
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses minutes', () => {
    expect(parseDuration('45m')).toBe(2700);
  });

  it('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses combined hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  it('parses combined minutes and seconds', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('parses all three units', () => {
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Empty duration string');
  });

  it('throws on whitespace only', () => {
    expect(() => parseDuration('   ')).toThrow('Empty duration string');
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('abc')).toThrow('Invalid duration format');
  });

  it('throws on invalid unit', () => {
    expect(() => parseDuration('1d')).toThrow('Invalid duration format');
  });

  it('throws on wrong order', () => {
    expect(() => parseDuration('30m1h')).toThrow('Invalid duration format');
  });

  it('throws on duplicate units', () => {
    expect(() => parseDuration('1h2h')).toThrow('Invalid duration format');
  });

  it('throws on all zeros', () => {
    expect(() => parseDuration('0h0m0s')).toThrow('Invalid duration format');
  });

  it('ignores surrounding whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });
});
```
