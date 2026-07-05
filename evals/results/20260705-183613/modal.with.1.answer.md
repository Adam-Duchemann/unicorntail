```html
<!-- Add this dialog element to your page -->
<dialog id="deleteConfirmDialog">
  <p>This action cannot be undone</p>
  <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px;">
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn" style="background-color: #dc2626; color: white;">Delete</button>
  </div>
</dialog>

<script>
  let pendingDeleteId = null;
  const dialog = document.getElementById('deleteConfirmDialog');
  const cancelBtn = document.getElementById('cancelBtn');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  function openDeleteConfirm(id) {
    pendingDeleteId = id;
    dialog.showModal();
  }

  cancelBtn.addEventListener('click', () => {
    dialog.close();
    pendingDeleteId = null;
  });

  confirmDeleteBtn.addEventListener('click', () => {
    deleteItem(pendingDeleteId);
    dialog.close();
    pendingDeleteId = null;
  });

  // Close dialog if user presses Escape
  dialog.addEventListener('cancel', () => {
    pendingDeleteId = null;
  });
</script>
```

**Update your delete button** from:
```html
<button onclick="deleteItem(id)">Delete</button>
```

to:
```html
<button onclick="openDeleteConfirm(id)">Delete</button>
```

The `<dialog>` element is native HTML5—no library needed. `showModal()` makes it modal (blocks interaction with the rest of the page), and `close()` dismisses it. Pressing Escape also cancels, which the last listener handles.
