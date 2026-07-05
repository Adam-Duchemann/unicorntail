```javascript
const express = require('express');
const app = express();

// Simple rate limiter middleware
const createRateLimiter = (maxRequests, windowMs) => {
  const requests = new Map();

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    const windowStart = now - windowMs;

    if (!requests.has(ip)) {
      requests.set(ip, { count: 1, resetTime: now + windowMs });
      return next();
    }

    const record = requests.get(ip);

    // Reset if window expired
    if (record.resetTime < now) {
      record.count = 1;
      record.resetTime = now + windowMs;
      return next();
    }

    record.count++;

    if (record.count > maxRequests) {
      const retryAfter = Math.ceil((record.resetTime - now) / 1000);
      res.set('Retry-After', retryAfter);
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: retryAfter
      });
    }

    next();
  };
};

// Apply rate limiter: 10 requests per 60 seconds
const messageRateLimiter = createRateLimiter(10, 60 * 1000);

app.post('/api/messages', messageRateLimiter, (req, res) => {
  // Your message handler
  res.json({ success: true });
});

app.listen(3000);
```

The middleware:
- Extracts client IP from `req.ip` (Express's parsed value, respects X-Forwarded-For if behind a proxy)
- Tracks request count and reset time per IP in a Map
- Resets the counter when the 60-second window expires
- Returns `429 Too Many Requests` with a `Retry-After` header when limit is exceeded
- No external dependencies

If you need persistence across restarts, you'd swap the Map for Redis, but for a single process this in-memory approach is fine.
