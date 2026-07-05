Here's a simple rate limiter middleware for your Express API:

```javascript
// Rate limiter middleware for single-process deployment
// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> use Redis or similar
const createRateLimiter = (maxRequests, windowMs) => {
  const clientRequests = new Map();

  return (req, res, next) => {
    const clientIp = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    const windowStart = now - windowMs;

    if (!clientRequests.has(clientIp)) {
      clientRequests.set(clientIp, []);
    }

    const requests = clientRequests.get(clientIp);
    const recentRequests = requests.filter(time => time > windowStart);

    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: Math.ceil((requests[0] + windowMs - now) / 1000)
      });
    }

    recentRequests.push(now);
    clientRequests.set(clientIp, recentRequests);
    next();
  };
};

// In your Express app:
const rateLimiter = createRateLimiter(10, 60 * 1000); // 10 requests per 60 seconds

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your message handling logic
});
```

How it works:
- Tracks request timestamps per IP in a `Map`
- On each request, filters out old timestamps outside the 60-second window
- Returns 429 if the limit is exceeded, with a `retryAfter` header
- Cleans up old data automatically by only keeping recent requests

For production with multiple processes, replace the `Map` with Redis using `express-rate-limit` or similar.
