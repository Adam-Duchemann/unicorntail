Here are two options:

**Option 1: Using `express-rate-limit` (recommended)**

```javascript
import rateLimit from 'express-rate-limit';

const messageLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute
  keyGenerator: (req) => req.ip, // Rate limit by IP
  standardHeaders: false,
  skip: (req) => {
    // Optional: skip rate limiting for certain IPs
    return false;
  },
  handler: (req, res) => {
    res.status(429).json({ error: 'Too many requests, try again later.' });
  },
});

app.post('/api/messages', messageLimiter, (req, res) => {
  // Your handler
});
```

Install: `npm install express-rate-limit`

---

**Option 2: Manual in-memory (no dependencies)**

```javascript
const ipLimits = new Map();

const simpleRateLimiter = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const windowStart = now - 60 * 1000;

  if (!ipLimits.has(ip)) {
    ipLimits.set(ip, []);
  }

  const timestamps = ipLimits.get(ip).filter(t => t > windowStart);
  
  if (timestamps.length >= 10) {
    return res.status(429).json({ error: 'Too many requests, try again later.' });
  }

  timestamps.push(now);
  ipLimits.set(ip, timestamps);
  next();
};

app.post('/api/messages', simpleRateLimiter, (req, res) => {
  // Your handler
});
```

**I'd go with Option 1** — `express-rate-limit` is battle-tested, handles trust proxy setups, and cleans old entries automatically. Option 2 requires a cleanup loop if you run for days (add a periodic `ipLimits.clear()` or filter on access).
