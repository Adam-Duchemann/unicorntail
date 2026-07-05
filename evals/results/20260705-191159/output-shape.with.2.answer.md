```javascript
const rateLimit = {};

const rateLimitMiddleware = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const oneMinuteAgo = now - 60000;
  
  if (!rateLimit[ip]) {
    rateLimit[ip] = [];
  }
  
  // Clean up old timestamps
  rateLimit[ip] = rateLimit[ip].filter(time => time > oneMinuteAgo);
  
  if (rateLimit[ip].length >= 10) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  
  rateLimit[ip].push(now);
  next();
};

app.post('/api/messages', rateLimitMiddleware, (req, res) => {
  // your handler
});
```

**Alternative:** If `express-rate-limit` is already installed:

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests
  keyGenerator: (req) => req.ip,
  handler: (req, res) => res.status(429).json({ error: 'Rate limit exceeded' })
});

app.post('/api/messages', limiter, (req, res) => {
  // your handler
});
```

**Skipped:** memory cleanup task (stale IPs stay in the store). Add when traffic grows or uptime matters — either periodic cleanup (`setInterval(() => { /* prune > 24h old */ }, 3600000)`) or switch to a Map with TTL.
