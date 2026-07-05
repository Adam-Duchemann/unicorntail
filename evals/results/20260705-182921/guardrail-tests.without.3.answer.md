```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Input must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Input must be a non-empty string');
  }

  let totalSeconds = 0;
  let i = 0;

  while (i < trimmed.length) {
    // Parse number
    let numStr = '';
    while (i < trimmed.length && /\d/.test(trimmed[i])) {
      numStr += trimmed[i];
      i++;
    }

    if (!numStr) {
      throw new Error(`Invalid format at position ${i}: expected a number`);
    }

    const num = parseInt(numStr, 10);

    // Parse unit
    if (i >= trimmed.length) {
      throw new Error(`Invalid format: number ${num} has no unit`);
    }

    const unit = trimmed[i];
    i++;

    switch (unit) {
      case 'h':
        totalSeconds += num * 3600;
        break;
      case 'm':
        totalSeconds += num * 60;
        break;
      case 's':
        totalSeconds += num;
        break;
      default:
        throw new Error(`Invalid unit '${unit}': expected 'h', 'm', or 's'`);
    }
  }

  return totalSeconds;
}

// Tests
const tests = [
  { input: '1h30m', expected: 5400 },
  { input: '45s', expected: 45 },
  { input: '2h', expected: 7200 },
  { input: '90m10s', expected: 5410 },
  { input: '1h', expected: 3600 },
  { input: '1m', expected: 60 },
  { input: '1s', expected: 1 },
  { input: '2h30m45s', expected: 9045 },
  { input: '0s', expected: 0 },
];

const invalidTests = [
  '',
  '  ',
  '45',
  '1h30',
  '1x',
  'h1m',
  '1h 30m',
  '1h30m45',
];

console.log('Valid tests:');
tests.forEach(({ input, expected }) => {
  const result = parseDuration(input);
  const pass = result === expected;
  console.log(`  ${pass ? '✓' : '✗'} parseDuration('${input}') = ${result} (expected ${expected})`);
});

console.log('\nInvalid tests (should throw):');
invalidTests.forEach((input) => {
  try {
    parseDuration(input);
    console.log(`  ✗ parseDuration('${input}') should have thrown but didn't`);
  } catch (e) {
    console.log(`  ✓ parseDuration('${input}') threw: ${(e as Error).message}`);
  }
});
```

The function:
- Iterates through the input string parsing number+unit pairs sequentially
- Converts each pair to seconds (h=3600, m=60, s=1) and accumulates
- Throws descriptive errors for: empty input, missing units, invalid units, incomplete format
- Supports any order and combination: "2h30m45s", "90m10s", "1h", etc.
