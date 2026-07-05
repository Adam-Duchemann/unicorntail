```js
const searchInput = document.querySelector('#search');
let debounceTimeout;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```

Each keystroke clears the previous timer and starts a new 300ms countdown. The API call fires only when typing stops for 300ms. Adjust the delay (third argument to `setTimeout`) as needed for your use case.
