Here's the confirmation dialog using the native `<dialog>` element:

```html
<!-- Add to your HTML -->
<dialog id="deleteConfirm">
  <p>This action cannot be undone</p>
  <button id="cancelBtn">Cancel</button>
  <button id="confirmDeleteBtn">Delete</button>
</dialog>

<!-- Your delete button calls this instead -->
<button onclick="showDeleteConfirm(itemId)">Delete</button>

<script>
const dialog = document.getElementById('deleteConfirm');
const cancelBtn = document.getElementById('cancelBtn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
let pendingDeleteId;

function showDeleteConfirm(id) {
  pendingDeleteId = id;
  dialog.showModal();
}

cancelBtn.addEventListener('click', () => dialog.close());

confirmDeleteBtn.addEventListener('click', () => {
  dialog.close();
  deleteItem(pendingDeleteId);
});
</script>
```

The `<dialog>` element handles the modal overlay, focus trapping, and Escape-to-close automatically. You can style the dialog with CSS if needed (e.g., `dialog { max-width: 400px; }`).
