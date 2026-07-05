```js
const searchInput = document.querySelector('#search');

let debounceTimer;
searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

The `clearTimeout` clears any pending API call, then `setTimeout` waits 300ms before fetching. If the user types again within that window, the timer resets and the previous call is cancelled.
