```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  const regex = /(\d+)([hms])/gi;
  const matches = [...trimmed.matchAll(regex)];

  if (matches.length === 0) {
    throw new Error(`Invalid input: no valid duration components found in "${trimmed}"`);
  }

  // Verify entire string was consumed by valid components
  const reconstructed = matches.map(m => m[0]).join('');
  if (reconstructed !== trimmed) {
    throw new Error(`Invalid input: unexpected characters in "${trimmed}"`);
  }

  let totalSeconds = 0;
  for (const match of matches) {
    const amount = parseInt(match[1], 10);
    const unit = match[2].toLowerCase();

    switch (unit) {
      case 'h':
        totalSeconds += amount * 3600;
        break;
      case 'm':
        totalSeconds += amount * 60;
        break;
      case 's':
        totalSeconds += amount;
        break;
    }
  }

  return totalSeconds;
}

// Tests
function assert(condition: boolean, message: string) {
  if (!condition) throw new Error(`Assertion failed: ${message}`);
}

function testParseDuration() {
  // Valid cases
  assert(parseDuration('45s') === 45, '45s');
  assert(parseDuration('1m') === 60, '1m');
  assert(parseDuration('1h') === 3600, '1h');
  assert(parseDuration('1h30m') === 5400, '1h30m');
  assert(parseDuration('2h') === 7200, '2h');
  assert(parseDuration('90m10s') === 5410, '90m10s');
  assert(parseDuration('1h30m45s') === 5445, '1h30m45s');
  assert(parseDuration('  1h30m  ') === 5400, 'handles whitespace');
  assert(parseDuration('1H30M45S') === 5445, 'case-insensitive');

  // Invalid cases
  try { parseDuration(''); throw new Error('Should throw'); } catch (e) { assert(e instanceof Error, 'empty string'); }
  try { parseDuration('invalid'); throw new Error('Should throw'); } catch (e) { assert(e instanceof Error, 'no components'); }
  try { parseDuration('1x'); throw new Error('Should throw'); } catch (e) { assert(e instanceof Error, 'invalid unit'); }
  try { parseDuration('1h 30m'); throw new Error('Should throw'); } catch (e) { assert(e instanceof Error, 'space chars'); }
  try { parseDuration('1h-30m'); throw new Error('Should throw'); } catch (e) { assert(e instanceof Error, 'dash chars'); }

  console.log('✓ All tests passed');
}

testParseDuration();
```
