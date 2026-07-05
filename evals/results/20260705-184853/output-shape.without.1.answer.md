No relevant prior context needed here — this is a standalone request. Here's an in-memory rate limiter for a single Node process:

```js
const rateLimitWindowMs = 60 * 1000; // 1 minute
const maxRequestsPerWindow = 10;
const requestLog = new Map(); // ip -> array of timestamps

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();

  const timestamps = (requestLog.get(ip) || []).filter(
    (ts) => now - ts < rateLimitWindowMs
  );

  if (timestamps.length >= maxRequestsPerWindow) {
    const retryAfterMs = rateLimitWindowMs - (now - timestamps[0]);
    res.set('Retry-After', Math.ceil(retryAfterMs / 1000));
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  timestamps.push(now);
  requestLog.set(ip, timestamps);
  next();
}

// Periodically clean up stale entries so the map doesn't grow unbounded
setInterval(() => {
  const now = Date.now();
  for (const [ip, timestamps] of requestLog) {
    const fresh = timestamps.filter((ts) => now - ts < rateLimitWindowMs);
    if (fresh.length === 0) {
      requestLog.delete(ip);
    } else {
      requestLog.set(ip, fresh);
    }
  }
}, rateLimitWindowMs).unref();

app.post('/api/messages', rateLimiter, (req, res) => {
  // existing handler
});
```

Notes:
- Make sure Express's `trust proxy` setting is correct if you're behind a reverse proxy/load balancer, or `req.ip` will be wrong.
- This is in-memory only — state resets on restart and won't work if you scale to multiple processes/instances later (you'd need Redis at that point).
