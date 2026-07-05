Here's a simple in-memory rate limiter for your Express API:

```javascript
// Rate limiter middleware
const createRateLimiter = () => {
  const requests = new Map(); // { ip: [timestamp1, timestamp2, ...] }
  const WINDOW_MS = 60 * 1000; // 1 minute
  const MAX_REQUESTS = 10;

  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();

    // Get or create request log for this IP
    if (!requests.has(ip)) {
      requests.set(ip, []);
    }

    const timestamps = requests.get(ip);

    // Remove timestamps outside the window
    const validTimestamps = timestamps.filter(ts => now - ts < WINDOW_MS);
    requests.set(ip, validTimestamps);

    // Check if limit exceeded
    if (validTimestamps.length >= MAX_REQUESTS) {
      return res.status(429).json({ error: 'Too many requests, please try again later' });
    }

    // Add current request
    validTimestamps.push(now);
    next();
  };
};

// Usage in your Express app
const app = require('express')();
const messageLimiter = createRateLimiter();

app.post('/api/messages', messageLimiter, (req, res) => {
  // Your message handling code
  res.json({ success: true });
});
```

This uses a `Map` to track timestamps per IP, cleaning old entries on each request. For a single Node process, this works well. If you need persistence across processes or more features (keys, skip logic, stores), use the `express-rate-limit` package instead:

```bash
npm install express-rate-limit
```

```javascript
const rateLimit = require('express-rate-limit');

const messageLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10,
  keyGenerator: (req) => req.ip,
  message: 'Too many requests, please try again later',
});

app.post('/api/messages', messageLimiter, (req, res) => {
  // Your message handling code
});
```

Which approach works better for your setup?
