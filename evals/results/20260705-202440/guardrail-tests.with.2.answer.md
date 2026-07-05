```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid input: must be a non-empty string');
  }

  const trimmed = input.trim();
  if (trimmed.length === 0) {
    throw new Error('Invalid input: empty string');
  }

  let totalSeconds = 0;
  let currentNum = '';
  
  for (let i = 0; i < trimmed.length; i++) {
    const char = trimmed[i];
    
    if (/\d/.test(char)) {
      currentNum += char;
    } else if (/[a-zA-Z]/.test(char)) {
      if (!currentNum) {
        throw new Error(`Invalid input: unit '${char}' has no number`);
      }
      
      const num = parseInt(currentNum, 10);
      
      switch (char.toLowerCase()) {
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
          throw new Error(`Invalid input: unknown unit '${char}'`);
      }
      
      currentNum = '';
    } else {
      throw new Error(`Invalid input: unexpected character '${char}'`);
    }
  }
  
  if (currentNum) {
    throw new Error('Invalid input: trailing number with no unit');
  }
  
  return totalSeconds;
}

// Tests
describe('parseDuration', () => {
  it('parses simple seconds', () => {
    expect(parseDuration('45s')).toBe(45);
  });

  it('parses simple minutes', () => {
    expect(parseDuration('2m')).toBe(120);
  });

  it('parses simple hours', () => {
    expect(parseDuration('1h')).toBe(3600);
  });

  it('parses combined hours and minutes', () => {
    expect(parseDuration('1h30m')).toBe(5400);
  });

  it('parses combined minutes and seconds', () => {
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('parses all three units', () => {
    expect(parseDuration('2h30m45s')).toBe(9045);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('throws on empty string', () => {
    expect(() => parseDuration('')).toThrow('Invalid input: empty string');
  });

  it('throws on unit with no number', () => {
    expect(() => parseDuration('h')).toThrow('Invalid input: unit \'h\' has no number');
  });

  it('throws on trailing number', () => {
    expect(() => parseDuration('1h30')).toThrow('Invalid input: trailing number with no unit');
  });

  it('throws on unknown unit', () => {
    expect(() => parseDuration('1x')).toThrow('Invalid input: unknown unit \'x\'');
  });

  it('throws on invalid characters', () => {
    expect(() => parseDuration('1h-30m')).toThrow('Invalid input: unexpected character \'-\'');
  });

  it('handles uppercase and lowercase units', () => {
    expect(parseDuration('1H30M45S')).toBe(9045);
    expect(parseDuration('1H')).toBe(3600);
  });

  it('parses zero values', () => {
    expect(parseDuration('0s')).toBe(0);
  });

  it('parses large numbers', () => {
    expect(parseDuration('100h')).toBe(360000);
  });
});
```
