No prior memory available for this. Here's a simple in-memory rate limiter middleware (fine for a single Node process):

```js
const rateLimitStore = new Map(); // ip -> { count, resetAt }

const RATE_LIMIT = 10;
const WINDOW_MS = 60 * 1000; // 1 minute

function messageRateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();

  let entry = rateLimitStore.get(ip);

  if (!entry || now >= entry.resetAt) {
    entry = { count: 0, resetAt: now + WINDOW_MS };
    rateLimitStore.set(ip, entry);
  }

  entry.count++;

  if (entry.count > RATE_LIMIT) {
    const retryAfterSec = Math.ceil((entry.resetAt - now) / 1000);
    res.set('Retry-After', String(retryAfterSec));
    return res.status(429).json({ error: 'Too many requests. Please try again later.' });
  }

  next();
}

// Periodically clean up expired entries so the Map doesn't grow unbounded
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of rateLimitStore) {
    if (now >= entry.resetAt) rateLimitStore.delete(ip);
  }
}, WINDOW_MS).unref();

module.exports = { messageRateLimiter };
```

Usage:

```js
const { messageRateLimiter } = require('./messageRateLimiter');

app.post('/api/messages', messageRateLimiter, (req, res) => {
  // your handler
});
```

Notes:
- `req.ip` requires `app.set('trust proxy', ...)` to be configured correctly if you're behind a reverse proxy/load balancer — otherwise all requests may appear to come from the proxy's IP.
- This resets per-IP counters on a fixed window (not sliding), so it's simple but allows brief bursts near window boundaries — fine for "simple" per your ask.
- Since it's in-memory, this won't work correctly if you scale to multiple processes/instances later (you'd need Redis or similar at that point).
