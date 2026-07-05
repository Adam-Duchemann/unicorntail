Here's a simple in-memory rate limiter for a single Node process:

```javascript
const requestCounts = new Map(); // IP -> {count, resetTime}

const rateLimit = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const minute = 60 * 1000;
  
  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, { count: 1, resetTime: now + minute });
    return next();
  }
  
  const record = requestCounts.get(ip);
  
  if (now > record.resetTime) {
    record.count = 1;
    record.resetTime = now + minute;
    return next();
  }
  
  if (record.count >= 10) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  record.count++;
  next();
};

app.post('/api/messages', rateLimit, (req, res) => {
  // your handler
});
```

**Alternative: if you have `express-rate-limit` installed:**

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10,
  keyGenerator: (req) => req.ip,
  message: 'Too many requests',
  status: 429,
});

app.post('/api/messages', limiter, (req, res) => {
  // your handler
});
```

The first solution has zero dependencies and works fine for single-process deployments. The second is production-proven if you already use the library.
