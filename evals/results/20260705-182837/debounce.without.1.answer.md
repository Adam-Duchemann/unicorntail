```js
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
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

The debounce function delays execution by 300ms (adjust as needed). Each keystroke cancels the previous timer, so the API call only fires after the user stops typing for 300ms.

Alternative inline approach without a utility function:

```js
const searchInput = document.querySelector('#search');
let timeoutId;

searchInput.addEventListener('input', (e) => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(renderResults);
  }, 300);
});
```
