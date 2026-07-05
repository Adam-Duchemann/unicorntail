```html
<dialog id="deleteDialog">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelDelete">Cancel</button>
    <button id="confirmDelete">Delete</button>
  </div>
</dialog>

<script>
const dialog = document.getElementById('deleteDialog');
const cancelBtn = document.getElementById('cancelDelete');
const confirmBtn = document.getElementById('confirmDelete');
let pendingId = null;

function deleteItem(id) {
  pendingId = id;
  dialog.showModal();
}

cancelBtn.onclick = () => dialog.close();
confirmBtn.onclick = () => {
  // your deletion logic here
  console.log('Deleting:', pendingId);
  dialog.close();
};
</script>

<style>
dialog {
  padding: 1.5rem;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
}
dialog p {
  margin: 0 0 1.5rem 0;
}
dialog div {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
dialog button {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  background: white;
}
dialog button#confirmDelete {
  background: #dc3545;
  color: white;
  border-color: #dc3545;
}
</style>
```

Uses native `<dialog>` element — no dependencies, keyboard-accessible (Esc closes), and handles button layout. Drop it in your HTML, replace the `console.log` with your deletion logic.
