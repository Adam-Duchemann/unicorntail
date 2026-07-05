```typescript
function parseDuration(input: string): number {
  const trimmed = input.trim().toLowerCase();
  
  if (!trimmed) {
    throw new Error('Invalid duration: empty input');
  }
  
  if (!/^(\d+[hms])+$/.test(trimmed)) {
    throw new Error(`Invalid duration format: "${input}"`);
  }

  let seconds = 0;
  const matches = trimmed.match(/(\d+)([hms])/g)!;
  
  for (const match of matches) {
    const [, value, unit] = /(\d+)([hms])/.exec(match)!;
    const num = parseInt(value, 10);
    
    switch (unit) {
      case 'h':
        seconds += num * 3600;
        break;
      case 'm':
        seconds += num * 60;
        break;
      case 's':
        seconds += num;
        break;
    }
  }
  
  return seconds;
}

// Tests
import { describe, it, expect } from 'vitest';

describe('parseDuration', () => {
  it('parses hours', () => {
    expect(parseDuration('1h')).toBe(3600);
    expect(parseDuration('2h')).toBe(7200);
  });

  it('parses minutes', () => {
    expect(parseDuration('30m')).toBe(1800);
    expect(parseDuration('90m')).toBe(5400);
  });

  it('parses seconds', () => {
    expect(parseDuration('45s')).toBe(45);
    expect(parseDuration('10s')).toBe(10);
  });

  it('parses combined durations', () => {
    expect(parseDuration('1h30m')).toBe(5400);
    expect(parseDuration('2h30m45s')).toBe(9045);
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
  });

  it('is case-insensitive', () => {
    expect(parseDuration('1H30M')).toBe(5400);
    expect(parseDuration('1H30m45S')).toBe(9045);
  });

  it('throws on invalid input', () => {
    expect(() => parseDuration('')).toThrow();
    expect(() => parseDuration('  ')).toThrow();
    expect(() => parseDuration('invalid')).toThrow();
    expect(() => parseDuration('1x')).toThrow();
    expect(() => parseDuration('h30m')).toThrow();
    expect(() => parseDuration('1.5h')).toThrow();
    expect(() => parseDuration('1h 30m')).toThrow();
  });
});
```

Regex `/^(\d+[hms])+$/` validates the entire string is only digits+unit pairs; regex `/(d+)([hms])/g` extracts each value/unit pair. Skipped custom errors for each unit — throws on parse with the format message.
