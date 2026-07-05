```js
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.querySelector('#search');
const debouncedSearch = debounce((query) => {
  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

The debounce function delays the API call by 300ms. If the user types again before the timer expires, it clears the previous timer and starts a new one, so the call only fires after they stop typing.
