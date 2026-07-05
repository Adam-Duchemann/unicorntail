Here's a simple in-memory rate limiter for your Express API:

```javascript
function createRateLimiter(maxRequests = 10, windowMs = 60000) {
  const requests = new Map();

  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    const windowStart = now - windowMs;

    if (!requests.has(ip)) {
      requests.set(ip, []);
    }

    const ipRequests = requests.get(ip);
    const recentRequests = ipRequests.filter(time => time > windowStart);

    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({ 
        error: 'Too many requests, please try again later.' 
      });
    }

    recentRequests.push(now);
    requests.set(ip, recentRequests);

    // Clean up old IPs periodically
    if (Math.random() < 0.01) {
      for (const [key, times] of requests.entries()) {
        if (times.filter(t => t > windowStart).length === 0) {
          requests.delete(key);
        }
      }
    }

    next();
  };
}

// Usage:
const rateLimiter = createRateLimiter(10, 60000); // 10 req/min
app.post('/api/messages', rateLimiter, (req, res) => {
  // your handler
});
```

For production, consider `express-rate-limit` package which handles distributed deployments, persistent stores, and has more features — but this works fine for a single process and has zero dependencies.
