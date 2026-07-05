```ts
export function formatTimeAgo(iso: string, locale: string): string {
  const now = new Date();
  const date = new Date(iso);
  const secondsElapsed = Math.floor((now.getTime() - date.getTime()) / 1000);

  const units: Array<[Intl.RelativeTimeFormatUnit, number]> = [
    ['year', 31536000],
    ['month', 2592000],
    ['week', 604800],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
    ['second', 1],
  ];

  for (const [unit, seconds] of units) {
    if (Math.abs(secondsElapsed) >= seconds) {
      const value = Math.round(secondsElapsed / seconds);
      return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-value, unit);
    }
  }

  return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(0, 'second');
}
```

Uses native `Intl.RelativeTimeFormat` for automatic locale handling. Negative value because the API expects past times as negative.
