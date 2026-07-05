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

The timer is cleared and reset on each keystroke, so the API call only fires 300ms after the user stops typing. Adjust the delay as needed.
