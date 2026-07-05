Add this function to your `src/utils/date.ts` file:

```ts
export function timeAgo(iso: string, locale: string): string {
  const date = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  
  const units: Array<[Intl.RelativeTimeFormatUnit, number]> = [
    ['year', 1000 * 60 * 60 * 24 * 365],
    ['month', 1000 * 60 * 60 * 24 * 30],
    ['week', 1000 * 60 * 60 * 24 * 7],
    ['day', 1000 * 60 * 60 * 24],
    ['hour', 1000 * 60 * 60],
    ['minute', 1000 * 60],
    ['second', 1000],
  ];
  
  for (const [unit, ms] of units) {
    if (diffMs >= ms) {
      return rtf.format(-Math.round(diffMs / ms), unit);
    }
  }
  
  return rtf.format(0, 'second');
}
```

Uses native `Intl.RelativeTimeFormat` (built-in since ES2020), no dependencies. Call it with `timeAgo(isoString, locale)` and it returns "3 minutes ago", "2 days ago", etc. in the user's language.
