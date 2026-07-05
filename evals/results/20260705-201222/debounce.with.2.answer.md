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

Or as a reusable function:

```js
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.querySelector('#search');
const debouncedSearch = debounce((e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', debouncedSearch);
```

The 300ms delay is a good default; adjust it based on your needs. The first approach is simpler for a single use case; the second lets you reuse the debounce logic elsewhere.
