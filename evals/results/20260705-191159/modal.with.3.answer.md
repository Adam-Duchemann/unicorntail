```html
<!-- Add this dialog to your page (can go at the end of body) -->
<dialog id="deleteConfirmDialog" style="border: none; border-radius: 8px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <h2 style="margin-top: 0;">Delete item?</h2>
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end;">
    <button onclick="document.getElementById('deleteConfirmDialog').close()" style="padding: 8px 16px; cursor: pointer;">Cancel</button>
    <button id="confirmDeleteBtn" style="padding: 8px 16px; cursor: pointer; background: #dc2626; color: white; border: none; border-radius: 4px;">Delete</button>
  </div>
</dialog>

<script>
  let itemToDelete = null;

  function showDeleteConfirm(id) {
    itemToDelete = id;
    document.getElementById('deleteConfirmDialog').showModal();
  }

  document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
    if (itemToDelete !== null) {
      deleteItem(itemToDelete);
      document.getElementById('deleteConfirmDialog').close();
      itemToDelete = null;
    }
  });
</script>
```

Then change your delete button from:
```html
<button onclick="deleteItem(id)">Delete</button>
```

To:
```html
<button onclick="showDeleteConfirm(id)">Delete</button>
```

The `<dialog>` element is native (no polyfill needed for modern browsers). Call `showDeleteConfirm(id)` instead of `deleteItem(id)` directly.
