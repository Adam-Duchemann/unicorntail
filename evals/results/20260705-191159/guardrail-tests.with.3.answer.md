```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Input must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Input cannot be empty');
  }

  let totalSeconds = 0;
  const pattern = /(\d+(?:\.\d+)?)\s*([hms])/gi;
  let lastEnd = 0;

  for (const match of trimmed.matchAll(pattern)) {
    // Check for unexpected characters between matches
    const gap = trimmed.slice(lastEnd, match.index).trim();
    if (gap) {
      throw new Error(`Invalid duration format: "${input}"`);
    }

    const value = parseFloat(match[1]);
    const unit = match[2].toLowerCase();

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

    lastEnd = match.index! + match[0].length;
  }

  // Check that we consumed the entire string
  const finalGap = trimmed.slice(lastEnd).trim();
  if (lastEnd === 0 || finalGap) {
    throw new Error(`Invalid duration format: "${input}"`);
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
  });

  it('handles spaces and case variations', () => {
    expect(parseDuration('1 h 30 m')).toBe(5400);
    expect(parseDuration('  1h30m  ')).toBe(5400);
    expect(parseDuration('1H30M')).toBe(5400);
  });

  it('handles decimal values', () => {
    expect(parseDuration('1.5h')).toBe(5400);
    expect(parseDuration('30.5s')).toBe(30.5);
  });

  it('throws on invalid formats', () => {
    expect(() => parseDuration('')).toThrow('cannot be empty');
    expect(() => parseDuration('  ')).toThrow('cannot be empty');
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('90m10s extra')).toThrow('Invalid duration format');
  });

  it('throws on null/undefined', () => {
    expect(() => parseDuration(null as any)).toThrow('must be a non-empty string');
    expect(() => parseDuration(undefined as any)).toThrow('must be a non-empty string');
  });
});
```

Regex validates format: `(\d+(?:\.\d+)?)\s*([hms])` matches optional-decimal number + optional spaces + unit. Entire input must be consumed by pattern matches (or throws). Skipped: negative-value checks (users usually don't pass them; add if needed).
