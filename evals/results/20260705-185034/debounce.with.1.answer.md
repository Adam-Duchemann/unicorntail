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

Each keystroke clears the pending request and resets the 300ms timer. The fetch only fires after the user stops typing for 300ms. Adjust the delay (third argument to `setTimeout`) as needed — 300ms is typical for search inputs.
