```javascript
const rateLimits = new Map();

function ipRateLimiter(req, res, next) {
  const ip = req.ip || req.connection.remoteAddress;
  const now = Date.now();
  const windowStart = now - 60000; // 1 minute in ms

  if (!rateLimits.has(ip)) {
    rateLimits.set(ip, []);
  }

  const timestamps = rateLimits.get(ip).filter(t => t > windowStart);

  if (timestamps.length >= 10) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  timestamps.push(now);
  rateLimits.set(ip, timestamps);
  next();
}

app.post('/api/messages', ipRateLimiter, (req, res) => {
  // Your handler
});
```

This uses an in-memory Map to track request timestamps per IP within a rolling 60-second window. Once an IP hits 10 requests in that window, it returns 429 (Too Many Requests).

**Ceiling:** The Map keeps entries for all IPs seen. For low-traffic APIs this is fine; if you need cleanup for high-traffic, add a periodic sweep: `setInterval(() => { const now = Date.now(); for (const [ip, ts] of rateLimits) { rateLimits.set(ip, ts.filter(t => t > now - 60000)); } }, 300000)`
