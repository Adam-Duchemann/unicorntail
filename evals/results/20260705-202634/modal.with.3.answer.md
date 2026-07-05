```html
<dialog id="confirmDialog">
  <p>This action cannot be undone.</p>
  <menu style="display:flex; gap:8px; justify-content:flex-end;">
    <button id="confirmCancelBtn" type="button">Cancel</button>
    <button id="confirmDeleteBtn" type="button">Delete</button>
  </menu>
</dialog>
```

```js
const confirmDialog = document.getElementById('confirmDialog');
let pendingDeleteId = null;

function confirmDelete(id) {
  pendingDeleteId = id;
  confirmDialog.showModal();
}

document.getElementById('confirmCancelBtn').addEventListener('click', () => {
  confirmDialog.close();
});

document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
  confirmDialog.close();
  deleteItem(pendingDeleteId);
});
```

Change your delete button from calling `deleteItem(id)` directly to `confirmDelete(id)`. Uses the native `<dialog>` element, so no library and no extra styling/animation code needed.
