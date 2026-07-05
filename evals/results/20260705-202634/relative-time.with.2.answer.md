Add this to `src/utils/date.ts` using `Intl.RelativeTimeFormat` (native stdlib, rung 3 — no new dependency needed):

```ts
const RELATIVE_TIME_DIVISIONS: { amount: number; unit: Intl.RelativeTimeFormatUnit }[] = [
  { amount: 60, unit: 'seconds' },
  { amount: 60, unit: 'minutes' },
  { amount: 24, unit: 'hours' },
  { amount: 7, unit: 'days' },
  { amount: 4.34524, unit: 'weeks' },
  { amount: 12, unit: 'months' },
  { amount: Infinity, unit: 'years' },
];

export function formatTimeAgo(iso: string, locale: string): string {
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  let duration = (new Date(iso).getTime() - Date.now()) / 1000;

  for (const division of RELATIVE_TIME_DIVISIONS) {
    if (Math.abs(duration) < division.amount) {
      return rtf.format(Math.round(duration), division.unit);
    }
    duration /= division.amount;
  }

  return rtf.format(Math.round(duration), 'years');
}
```

Usage: `formatTimeAgo(item.createdAt, locale)` → e.g. `"il y a 3 minutes"` for `locale="fr"`, `"3 minutes ago"` for `"en"`.

Notes:
- `numeric: 'auto'` gives idiomatic "yesterday"/"hier" instead of "1 day ago" where the locale supports it.
- Negative `duration` (past timestamps) naturally produces "ago" phrasing; it'll also correctly say "in 3 minutes" if you ever get a future timestamp (clock skew).
- `Intl.RelativeTimeFormat` has been supported in all evergreen browsers and Node since ~2020, so no polyfill needed.
