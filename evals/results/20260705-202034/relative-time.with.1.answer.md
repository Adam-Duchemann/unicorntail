```ts
const RTF_UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['year', 60 * 60 * 24 * 365],
  ['month', 60 * 60 * 24 * 30],
  ['week', 60 * 60 * 24 * 7],
  ['day', 60 * 60 * 24],
  ['hour', 60 * 60],
  ['minute', 60],
  ['second', 1],
];

export function timeAgo(iso: string, locale: string): string {
  const seconds = (new Date(iso).getTime() - Date.now()) / 1000;
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  for (const [unit, unitSeconds] of RTF_UNITS) {
    if (Math.abs(seconds) >= unitSeconds || unit === 'second') {
      return rtf.format(Math.round(seconds / unitSeconds), unit);
    }
  }
  return rtf.format(0, 'second');
}
```

`Intl.RelativeTimeFormat` is built into JS — no dependency needed. Drop it into `src/utils/date.ts` alongside `formatDate`.
