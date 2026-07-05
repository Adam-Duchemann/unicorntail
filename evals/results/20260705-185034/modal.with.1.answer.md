```html
<!-- Add this dialog to your page -->
<dialog id="deleteConfirmDialog">
  <h2>Delete Item</h2>
  <p>This action cannot be undone.</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px;">
    <button id="cancelBtn">Cancel</button>
    <button id="deleteBtn">Delete</button>
  </div>
</dialog>
```

```javascript
let itemToDelete = null;

function showDeleteConfirmation(id) {
  itemToDelete = id;
  document.getElementById('deleteConfirmDialog').showModal();
}

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('deleteConfirmDialog').close();
  itemToDelete = null;
});

document.getElementById('deleteBtn').addEventListener('click', () => {
  deleteItem(itemToDelete);
  document.getElementById('deleteConfirmDialog').close();
  itemToDelete = null;
});
```

Then change your delete button from `onclick="deleteItem(id)"` to `onclick="showDeleteConfirmation(id)"`.

The native `<dialog>` element handles backdrop focus, keyboard escape, and accessibility automatically. Style `.deleteConfirmDialog` with CSS if needed for colors/sizing.
