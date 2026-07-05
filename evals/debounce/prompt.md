Add debounce to a search input in vanilla JavaScript. It currently fires an API call on every keystroke:

```js
const searchInput = document.querySelector('#search');
searchInput.addEventListener('input', (e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
});
```

Reply with the code directly. Do not create files.
