```html
<!-- Add this dialog to your HTML -->
<dialog id="deleteConfirmDialog">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn" style="color: red;">Delete</button>
  </div>
</dialog>
```

```javascript
const dialog = document.getElementById('deleteConfirmDialog');
const cancelBtn = document.getElementById('cancelBtn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
let pendingDeleteId = null;

// Show dialog when user clicks delete
function showDeleteConfirm(id) {
  pendingDeleteId = id;
  dialog.showModal();
}

// Cancel button closes dialog
cancelBtn.addEventListener('click', () => {
  dialog.close();
  pendingDeleteId = null;
});

// Confirm button actually deletes
confirmDeleteBtn.addEventListener('click', () => {
  if (pendingDeleteId !== null) {
    deleteItem(pendingDeleteId);
    dialog.close();
    pendingDeleteId = null;
  }
});
```

Then change your delete button from:
```html
<button onclick="deleteItem(id)">Delete</button>
```

To:
```html
<button onclick="showDeleteConfirm(id)">Delete</button>
```

The `<dialog>` element is native browser API — no library needed. `showModal()` shows it as a modal (blocks interaction with the rest of the page), and `close()` dismisses it.
