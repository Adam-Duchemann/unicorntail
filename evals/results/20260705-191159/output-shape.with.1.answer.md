```javascript
const rateLimits = new Map();

const rateLimitMiddleware = (req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  const windowStart = now - 60000; // 1 minute
  
  if (!rateLimits.has(ip)) {
    rateLimits.set(ip, []);
  }
  
  const timestamps = rateLimits.get(ip);
  const recent = timestamps.filter(t => t > windowStart);
  
  if (recent.length >= 10) {
    return res.status(429).json({ error: 'Rate limit exceeded: max 10 requests per minute' });
  }
  
  recent.push(now);
  rateLimits.set(ip, recent);
  next();
};

app.post('/api/messages', rateLimitMiddleware, (req, res) => {
  // your handler
});
```

This tracks request timestamps per IP in memory and filters out entries older than 60 seconds on each request. Skipped: external dependency (works with just Node), cleanup (garbage-collected when entries age out naturally), and per-endpoint config (hardcoded 10/minute; parameterize if you add more routes). For higher scale, swap this for `express-rate-limit` package.
