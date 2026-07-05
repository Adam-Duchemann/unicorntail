```js
const searchInput = document.querySelector('#search');
let searchTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

This clears any pending timeout on each keystroke and starts a new one, so the API call fires only 300ms after the user stops typing. Adjust the delay as needed.
