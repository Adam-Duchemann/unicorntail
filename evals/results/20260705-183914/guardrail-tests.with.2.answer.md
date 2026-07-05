```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: expected non-empty string');
  }

  const trimmed = input.trim();
  if (!trimmed) {
    throw new Error('Invalid input: empty string');
  }

  let totalSeconds = 0;
  let currentNumber = '';

  for (let i = 0; i < trimmed.length; i++) {
    const char = trimmed[i];

    if (/\d/.test(char)) {
      currentNumber += char;
    } else if (char === 'h' || char === 'm' || char === 's') {
      if (!currentNumber) {
        throw new Error(`Invalid input: unit '${char}' without a number`);
      }

      const value = parseInt(currentNumber, 10);

      if (char === 'h') {
        totalSeconds += value * 3600;
      } else if (char === 'm') {
        totalSeconds += value * 60;
      } else if (char === 's') {
        totalSeconds += value;
      }

      currentNumber = '';
    } else {
      throw new Error(`Invalid input: unexpected character '${char}'`);
    }
  }

  if (currentNumber) {
    throw new Error('Invalid input: number without unit');
  }

  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  it('should parse single unit durations', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('2h')).toBe(7200);
    expect(parseDuration('5m')).toBe(300);
  });

  it('should parse multiple unit durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('90m10s')).toBe(5410);
    expect(parseDuration('1h30m45s')).toBe(5445);
  });

  it('should handle leading/trailing whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('should throw on invalid input', () => {
    expect(() => parseDuration('')).toThrow('Invalid input: empty string');
    expect(() => parseDuration('  ')).toThrow('Invalid input: empty string');
    expect(() => parseDuration('30')).toThrow('Invalid input: number without unit');
    expect(() => parseDuration('h30m')).toThrow("Invalid input: unit 'h' without a number");
    expect(() => parseDuration('30x')).toThrow("Invalid input: unexpected character 'x'");
    expect(() => parseDuration('1h 30m')).toThrow("Invalid input: unexpected character ' '");
  });

  it('should return 0 for zero duration', () => {
    expect(parseDuration('0s')).toBe(0);
  });
});
```
