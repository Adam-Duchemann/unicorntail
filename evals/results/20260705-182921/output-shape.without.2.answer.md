Here's a simple rate limiter using `express-rate-limit` (install with `npm install express-rate-limit`):

```javascript
const express = require('express');
const rateLimit = require('express-rate-limit');

const app = express();

// Rate limiter: 10 requests per minute per IP
const messagesLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests
  keyGenerator: (req, res) => req.ip,
  handler: (req, res) => {
    res.status(429).json({ error: 'Too many requests, try again later' });
  },
  skip: (req, res) => false, // Apply to all requests
});

// Apply limiter only to POST /api/messages
app.post('/api/messages', messagesLimiter, (req, res) => {
  // Your handler here
  res.json({ success: true });
});

app.listen(3000);
```

---

**Or, a simple built-in alternative** (no dependencies):

```javascript
const express = require('express');
const app = express();

const requestCounts = new Map(); // { ip: { count, resetTime } }

function rateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();
  const data = requestCounts.get(ip);

  if (data && now < data.resetTime) {
    if (data.count >= 10) {
      return res.status(429).json({ error: 'Too many requests, try again later' });
    }
    data.count++;
  } else {
    requestCounts.set(ip, { count: 1, resetTime: now + 60 * 1000 });
  }

  next();
}

app.post('/api/messages', rateLimiter, (req, res) => {
  // Your handler here
  res.json({ success: true });
});

app.listen(3000);
```

The first approach is cleaner and production-ready. The second is zero-dependency and will work fine for a single process with moderate traffic.
