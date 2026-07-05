```html
<!-- Add this dialog to your page -->
<dialog id="deleteConfirm">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn">Delete</button>
  </div>
</dialog>

<!-- Change your delete button from onclick="deleteItem(id)" to: -->
<button onclick="showDeleteConfirm(id)">Delete</button>
```

```javascript
let itemToDelete;

function showDeleteConfirm(id) {
  itemToDelete = id;
  document.getElementById('deleteConfirm').showModal();
}

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('deleteConfirm').close();
});

document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
  deleteItem(itemToDelete);
  document.getElementById('deleteConfirm').close();
});
```

Uses the native `<dialog>` element (built-in, no dependency). Replace `id` in the button's `onclick` with your actual variable containing the item ID.
