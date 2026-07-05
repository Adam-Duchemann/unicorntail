Here's a simple in-memory rate limiter for your use case:

```javascript
const createRateLimiter = (maxRequests, windowMs) => {
  const requests = new Map();

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    
    if (!requests.has(ip)) {
      requests.set(ip, []);
    }

    const timestamps = requests.get(ip);
    const recentRequests = timestamps.filter(t => now - t < windowMs);
    
    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }

    recentRequests.push(now);
    requests.set(ip, recentRequests);
    next();
  };
};

// Apply to route
const limiter = createRateLimiter(10, 60 * 1000); // 10 requests per minute
app.post('/api/messages', limiter, (req, res) => {
  // Your handler
});
```

**Or use the popular `express-rate-limit` package** (more robust, handles edge cases):

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per windowMs
  keyGenerator: (req) => req.ip || req.connection.remoteAddress,
  handler: (req, res) => res.status(429).json({ error: 'Too many requests' }),
});

app.post('/api/messages', limiter, (req, res) => {
  // Your handler
});
```

For a single Node process, either works fine. The custom version is lightweight; `express-rate-limit` handles IP detection, cleanup, and edge cases automatically. Pick based on your dependency preferences.
