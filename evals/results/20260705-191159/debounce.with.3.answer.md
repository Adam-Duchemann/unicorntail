```js
const searchInput = document.querySelector('#search');
let debounceTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300); // Adjust delay (ms) as needed
});
```

The `clearTimeout` cancels the previous pending call on each keystroke, and `setTimeout` queues a new one. The API only fires if 300ms pass without another keystroke. Tune the delay to your needs.
