```js
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.querySelector('#search');

const handleSearch = debounce((e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300);

searchInput.addEventListener('input', handleSearch);
```

The debounce helper clears the timeout each keystroke, so the API call only fires 300ms after the user stops typing. Adjust the delay (third argument) as needed.

If you want to also cancel in-flight requests, you can use `AbortController`:

```js
const searchInput = document.querySelector('#search');
let abortController = null;

function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const handleSearch = debounce((e) => {
  if (abortController) abortController.abort();
  abortController = new AbortController();
  
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`, { signal: abortController.signal })
    .then(r => r.json())
    .then(renderResults)
    .catch(err => err.name !== 'AbortError' && console.error(err));
}, 300);

searchInput.addEventListener('input', handleSearch);
```

This prevents older requests from overwriting newer results if they complete out of order.
