```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  let totalSeconds = 0;
  const regex = /(\d+)([hms])/g;
  let match;
  let lastIndex = 0;

  while ((match = regex.exec(trimmed)) !== null) {
    const value = parseInt(match[1], 10);
    const unit = match[2];

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

    lastIndex = match.index + match[0].length;
  }

  if (lastIndex === 0 || lastIndex !== trimmed.length) {
    throw new Error(`Invalid duration format: ${input}`);
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  it('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses minutes', () => {
    expect(parseDuration('2m')).toBe(120);
  });

  it('parses hours', () => {
    expect(parseDuration('1h')).toBe(3600);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('1h30m45s')).toBe(5445);
    expect(parseDuration('2h10m30s')).toBe(7830);
  });

  it('parses zero values', () => {
    expect(parseDuration('0s')).toBe(0);
    expect(parseDuration('0h0m0s')).toBe(0);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Invalid input: empty string');
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('abc123')).toThrow('Invalid duration format');
  });

  it('throws on partial invalid match', () => {
    expect(() => parseDuration('1h invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h 30m')).toThrow('Invalid duration format');
  });

  it('throws on null/non-string input', () => {
    expect(() => parseDuration(null as any)).toThrow('Invalid input');
    expect(() => parseDuration(undefined as any)).toThrow('Invalid input');
  });
});
```

The function uses a regex to extract all `<number><unit>` pairs, validates that the entire input is consumed (catching invalid characters), converts each part to seconds, and throws on any malformation. Tests cover valid cases, edge cases, and all error paths.
