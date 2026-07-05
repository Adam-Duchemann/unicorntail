```js
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
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

The `debounce` function wraps your search callback and resets the timeout on each keystroke—the API call fires only once after 300ms of inactivity. Adjust the delay as needed.
