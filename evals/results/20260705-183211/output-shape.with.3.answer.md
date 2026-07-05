Here's a simple rate limiter using the `express-rate-limit` package (most practical for production):

```javascript
const rateLimit = require('express-rate-limit');

const messageLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute
  keyGenerator: (req, res) => req.ip,
  handler: (req, res) => {
    res.status(429).json({ error: 'Too many requests, please try again later.' });
  },
  standardHeaders: false,
  legacyHeaders: false,
});

app.post('/api/messages', messageLimiter, (req, res) => {
  // Your handler
});
```

Install with: `npm install express-rate-limit`

---

**Alternative: minimal custom implementation** (no dependencies):

```javascript
const ipRequestLog = new Map();

const rateLimiter = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const oneMinuteAgo = now - 60 * 1000;

  if (!ipRequestLog.has(ip)) {
    ipRequestLog.set(ip, []);
  }

  const timestamps = ipRequestLog.get(ip).filter(t => t > oneMinuteAgo);
  ipRequestLog.set(ip, timestamps);

  if (timestamps.length >= 10) {
    return res.status(429).json({ error: 'Too many requests, please try again later.' });
  }

  timestamps.push(now);
  next();
};

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler
});
```

Use the library version for simplicity; the custom version works fine for single-process deployments but the library is more battle-tested.
