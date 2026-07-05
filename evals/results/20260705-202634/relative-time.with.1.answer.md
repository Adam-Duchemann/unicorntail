```ts
const TIME_AGO_DIVISIONS: { amount: number; unit: Intl.RelativeTimeFormatUnit }[] = [
  { amount: 60, unit: 'seconds' },
  { amount: 60, unit: 'minutes' },
  { amount: 24, unit: 'hours' },
  { amount: 7, unit: 'days' },
  { amount: 4.34524, unit: 'weeks' },
  { amount: 12, unit: 'months' },
  { amount: Number.POSITIVE_INFINITY, unit: 'years' },
];

export function formatTimeAgo(iso: string, locale: string): string {
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  let duration = (new Date(iso).getTime() - Date.now()) / 1000;

  for (const division of TIME_AGO_DIVISIONS) {
    if (Math.abs(duration) < division.amount) {
      return rtf.format(Math.round(duration), division.unit);
    }
    duration /= division.amount;
  }

  return rtf.format(Math.round(duration), 'years');
}
```

Uses `Intl.RelativeTimeFormat` (stdlib, rung 3) — no new dependency. `numeric: 'auto'` gives idiomatic output like "yesterday"/"il y a 2 jours" instead of always "1 day ago". Divisions walk seconds→years, dividing the running duration down each step, same pattern as the MDN reference implementation.
