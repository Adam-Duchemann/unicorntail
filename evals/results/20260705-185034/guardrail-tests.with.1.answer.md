```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Input must be a non-empty string');
  }

  const normalized = input.toLowerCase().trim();
  
  // Match pattern: digits/decimals followed by h, m, or s
  const pattern = /(\d+(?:\.\d+)?)[hms]/g;
  const matches = Array.from(normalized.matchAll(pattern));
  
  if (matches.length === 0) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  // Ensure entire string was matched (no leftover characters)
  const matchedText = matches.map(m => m[0]).join('');
  if (matchedText !== normalized) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let totalSeconds = 0;
  const seenUnits = new Set<string>();

  for (const match of matches) {
    const value = parseFloat(match[1]);
    const unit = match[0].slice(-1);

    if (seenUnits.has(unit)) {
      throw new Error(`Duplicate unit "${unit}" in duration: "${input}"`);
    }
    seenUnits.add(unit);

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
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  const tests: Array<{ input: string; expected: number }> = [
    { input: '1h30m', expected: 5400 },
    { input: '45s', expected: 45 },
    { input: '2h', expected: 7200 },
    { input: '90m10s', expected: 5410 },
    { input: '1h', expected: 3600 },
    { input: '30m', expected: 1800 },
    { input: '1s', expected: 1 },
    { input: '1h30m45s', expected: 5445 },
    { input: '0.5h', expected: 1800 },
    { input: '2.5m', expected: 150 },
    { input: '  1h30m  ', expected: 5400 }, // with whitespace
    { input: '1H30M', expected: 5400 }, // uppercase
  ];

  test.each(tests)('converts "$input" to $expected seconds', ({ input, expected }) => {
    expect(parseDuration(input)).toBe(expected);
  });

  const errorCases = [
    '',
    '  ',
    'invalid',
    '1',
    '1h2',
    'h30m',
    '1x',
    '1h 30m',
    'abc',
    '1h1h', // duplicate unit
    '30m60m', // duplicate unit
  ];

  test.each(errorCases)('throws on invalid input: "$input"', (input) => {
    expect(() => parseDuration(input)).toThrow();
  });
});
```

Key features:
- **Parses combined units**: "1h30m45s" → 5445 seconds
- **Handles decimals**: "0.5h" → 1800 seconds
- **Case-insensitive**: "1H30M" works
- **Strips whitespace**: "  1h30m  " works
- **Validates strictly**: rejects "1h 30m" (space between), "1x" (invalid unit), "1h1h" (duplicate unit)
- **Throws on all invalid input**: empty strings, non-matching patterns, malformed input
- **Comprehensive tests**: positive cases, edge cases (decimals, whitespace), error cases
