```typescript
function parseDuration(input: string): number {
  if (!input || typeof input !== 'string') {
    throw new Error('Invalid duration format');
  }

  const trimmed = input.trim().toLowerCase();
  if (!trimmed) {
    throw new Error('Invalid duration format');
  }

  const regex = /(\d+)([hms])/g;
  let match;
  let totalSeconds = 0;
  let lastIndex = 0;
  const seenUnits = new Set<string>();

  while ((match = regex.exec(trimmed)) !== null) {
    if (match.index !== lastIndex) {
      throw new Error('Invalid duration format');
    }
    lastIndex = match.index + match[0].length;

    const value = parseInt(match[1], 10);
    const unit = match[2];

    if (seenUnits.has(unit)) {
      throw new Error('Invalid duration format');
    }
    seenUnits.add(unit);

    if (unit === 'h') {
      totalSeconds += value * 3600;
    } else if (unit === 'm') {
      totalSeconds += value * 60;
    } else if (unit === 's') {
      totalSeconds += value;
    }
  }

  if (lastIndex !== trimmed.length) {
    throw new Error('Invalid duration format');
  }

  if (totalSeconds === 0) {
    throw new Error('Invalid duration format');
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
    expect(parseDuration('2h45m30s')).toBe(9930);
    expect(parseDuration('90m10s')).toBe(5410);
  });

  it('handles whitespace', () => {
    expect(parseDuration('  1h30m  ')).toBe(5400);
    expect(parseDuration('\t2h\n')).toBe(7200);
  });

  it('is case-insensitive', () => {
    expect(parseDuration('1H')).toBe(3600);
    expect(parseDuration('30M')).toBe(1800);
  });

  it('throws on empty input', () => {
    expect(() => parseDuration('')).toThrow('Invalid duration format');
    expect(() => parseDuration('   ')).toThrow('Invalid duration format');
  });

  it('throws on invalid format', () => {
    expect(() => parseDuration('invalid')).toThrow('Invalid duration format');
    expect(() => parseDuration('1x')).toThrow('Invalid duration format');
    expect(() => parseDuration('1 h')).toThrow('Invalid duration format');
  });

  it('throws on duplicate units', () => {
    expect(() => parseDuration('1h2h')).toThrow('Invalid duration format');
    expect(() => parseDuration('30m20m')).toThrow('Invalid duration format');
  });

  it('throws on zero duration', () => {
    expect(() => parseDuration('0h')).toThrow('Invalid duration format');
    expect(() => parseDuration('0s')).toThrow('Invalid duration format');
  });
});
```
