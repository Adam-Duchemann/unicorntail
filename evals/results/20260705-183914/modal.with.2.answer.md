```html
<!-- Add this HTML where you want the dialog to appear -->
<dialog id="deleteConfirmDialog" style="border: 1px solid #ccc; border-radius: 8px; padding: 20px; min-width: 300px;">
  <h2 style="margin-top: 0; font-size: 1.1em;">Delete Item?</h2>
  <p style="color: #666;">This action cannot be undone</p>
  <div style="display: flex; gap: 10px; justify-content: flex-end;">
    <button id="cancelBtn" style="padding: 8px 16px; cursor: pointer;">Cancel</button>
    <button id="confirmDeleteBtn" style="padding: 8px 16px; background-color: #dc2626; color: white; border: none; border-radius: 4px; cursor: pointer;">Delete</button>
  </div>
</dialog>

<script>
  let itemToDelete = null;
  const dialog = document.getElementById('deleteConfirmDialog');
  const cancelBtn = document.getElementById('cancelBtn');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  // Modify your delete button handler
  function showDeleteConfirm(id) {
    itemToDelete = id;
    dialog.showModal();
  }

  cancelBtn.addEventListener('click', () => {
    dialog.close();
    itemToDelete = null;
  });

  confirmDeleteBtn.addEventListener('click', () => {
    if (itemToDelete !== null) {
      deleteItem(itemToDelete);
      dialog.close();
      itemToDelete = null;
    }
  });
</script>
```

Change your delete button from `onclick="deleteItem(id)"` to `onclick="showDeleteConfirm(id)"`. The `<dialog>` element is native HTML5 and handles modality (backdrop, focus trapping) automatically.
