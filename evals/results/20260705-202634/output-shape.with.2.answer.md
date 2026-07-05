Here's a simple in-memory rate limiter middleware:

```js
const rateLimitWindowMs = 60_000;
const rateLimitMax = 10;
const requestLog = new Map(); // ponytail: in-memory store, ceiling: single process (resets on restart, no cross-instance sharing), upgrade when: running >1 Node process -> shared store (e.g. Redis)

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const windowStart = now - rateLimitWindowMs;

  const timestamps = (requestLog.get(ip) || []).filter(t => t > windowStart);

  if (timestamps.length >= rateLimitMax) {
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  timestamps.push(now);
  requestLog.set(ip, timestamps);
  next();
}

app.post('/api/messages', rateLimiter, (req, res) => {
  // existing handler
});
```

skipped: periodic cleanup of stale IP entries in `requestLog`, add when memory growth from many distinct IPs becomes a problem.

Note: if Express sits behind a proxy/load balancer, set `app.set('trust proxy', true)` so `req.ip` reflects the real client IP rather than the proxy's.
