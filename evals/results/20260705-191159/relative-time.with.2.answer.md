```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const then = new Date(iso);
  const seconds = Math.floor((now.getTime() - then.getTime()) / 1000);

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 },
  ] as const;

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  for (const { label, seconds: interval } of intervals) {
    const count = Math.floor(seconds / interval);
    if (count >= 1) {
      return rtf.format(-count, label);
    }
  }

  return rtf.format(0, 'second');
}
```

Uses `Intl.RelativeTimeFormat` (native, no deps) to handle all localization—"3 minutes ago" in English, "hace 3 minutos" in Spanish, etc.
