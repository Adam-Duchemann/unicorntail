Add this to `src/utils/date.ts` — `Intl.RelativeTimeFormat` is built into JS and handles the locale-specific phrasing ("il y a 3 minutes", etc.) with no extra dependency:

```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const diffSeconds = (new Date(iso).getTime() - Date.now()) / 1000;
  const units: [Intl.RelativeTimeFormatUnit, number][] = [
    ['year', 60 * 60 * 24 * 365],
    ['month', 60 * 60 * 24 * 30],
    ['week', 60 * 60 * 24 * 7],
    ['day', 60 * 60 * 24],
    ['hour', 60 * 60],
    ['minute', 60],
    ['second', 1],
  ];

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  for (const [unit, secondsInUnit] of units) {
    if (Math.abs(diffSeconds) >= secondsInUnit || unit === 'second') {
      return rtf.format(Math.round(diffSeconds / secondsInUnit), unit);
    }
  }
  return rtf.format(0, 'second');
}
```

Call it as `formatTimeAgo(item.createdAt, locale)`. `numeric: 'auto'` gets you idiomatic phrasing like "yesterday" instead of "1 day ago" where the locale supports it.
