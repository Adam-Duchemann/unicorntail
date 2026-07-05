```javascript
const rateLimit = (() => {
  // ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store
  const requests = new Map(); // ip -> { count, resetAt }
  
  return (req, res, next) => {
    const ip = req.ip;
    const now = Date.now();
    let record = requests.get(ip);
    
    if (!record || now >= record.resetAt) {
      record = { count: 0, resetAt: now + 60000 };
    }
    
    record.count++;
    requests.set(ip, record);
    
    if (record.count > 10) {
      return res.status(429).json({ error: 'Too many requests' });
    }
    
    next();
  };
})();

app.post('/api/messages', rateLimit, (req, res) => {
  // Your handler
});
```

Tracks requests per IP in memory, resets the window independently for each IP after 60 seconds, and returns 429 when the limit is exceeded. When you scale to multiple processes, swap this for a shared store (Redis is the standard choice).
