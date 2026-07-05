```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Input must be a non-empty string');
  }

  const trimmed = input.trim().toLowerCase();
  
  const unitPattern = /(\d+)([dhms])/g;
  const matches = Array.from(trimmed.matchAll(unitPattern));

  // Validate that we matched the entire string (no invalid characters)
  const matchedString = matches.map(m => m[0]).join('');
  if (matches.length === 0 || matchedString !== trimmed) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  const seen = new Set<string>();

  for (const match of matches) {
    const [, value, suffix] = match;
    const num = parseInt(value, 10);

    if (seen.has(suffix)) {
      throw new Error(`Duplicate unit "${suffix}" in duration: "${input}"`);
    }
    seen.add(suffix);

    switch (suffix) {
      case 'd':
        totalSeconds += num * 86400;
        break;
      case 'h':
        totalSeconds += num * 3600;
        break;
      case 'm':
        totalSeconds += num * 60;
        break;
      case 's':
        totalSeconds += num;
        break;
    }
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  test('parses simple units', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2m')).toBe(120);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('1d')).toBe(86400);
  });

  test('parses compound durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1d2h30m45s')).toBe(95445);
  });

  test('handles uppercase', () => {
    expect(parseDuration('1H30M')).toBe(5400);
  });

  test('throws on invalid input', () => {
    expect(() => parseDuration('')).toThrow('Invalid duration format');
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1h 30m')).toThrow('Invalid duration format');
  });

  test('throws on duplicate units', () => {
    expect(() => parseDuration('1h2h')).toThrow('Duplicate unit "h"');
  });
});
```
