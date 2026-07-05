```js
const searchInput = document.querySelector('#search');
let timeoutId;

searchInput.addEventListener('input', (e) => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

This delays the fetch by 300ms, restarting the timer on each keystroke. Replace `300` with your desired delay in milliseconds.
