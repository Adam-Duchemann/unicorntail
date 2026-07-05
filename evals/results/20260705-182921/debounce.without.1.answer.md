Here's a debounced version using `setTimeout`:

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

Or with a reusable debounce function:

```js
function debounce(func, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => func(...args), delay);
  };
}

const searchInput = document.querySelector('#search');
const search = debounce((query) => {
  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', (e) => {
  search(e.target.value);
});
```

The 300ms delay is typical—adjust to your needs. Each keystroke cancels the previous timer and starts a new one, so the API only fires after the user pauses typing.
