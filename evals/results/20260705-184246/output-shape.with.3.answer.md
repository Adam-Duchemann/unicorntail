Here's a minimal in-memory rate limiter for your single-process setup:

```javascript
const rateLimit = {};

function createRateLimiter(maxRequests, windowMs) {
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    
    if (!rateLimit[ip]) {
      rateLimit[ip] = [];
    }
    
    // Remove timestamps outside the window
    rateLimit[ip] = rateLimit[ip].filter(time => now - time < windowMs);
    
    if (rateLimit[ip].length >= maxRequests) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    rateLimit[ip].push(now);
    next();
  };
}

app.post('/api/messages', createRateLimiter(10, 60000), (req, res) => {
  // Your handler
});
```

This creates a middleware that:
- Tracks request timestamps per IP in memory
- Removes timestamps older than 60 seconds
- Rejects with 429 if the limit is exceeded
- No external dependencies

If you prefer a package, `express-rate-limit` is a drop-in alternative:
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  keyGenerator: (req) => req.ip,
  handler: (req, res) => res.status(429).json({ error: 'Too many requests' })
});

app.post('/api/messages', limiter, (req, res) => {
  // Your handler
});
```
