```html
<dialog id="deleteConfirm">
  <h2>Delete Item</h2>
  <p>This action cannot be undone.</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn">Delete</button>
  </div>
</dialog>
```

```javascript
let itemToDelete = null;
const dialog = document.getElementById('deleteConfirm');

function showDeleteConfirm(id) {
  itemToDelete = id;
  dialog.showModal();
}

document.getElementById('cancelBtn').addEventListener('click', () => {
  dialog.close();
});

document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
  if (itemToDelete !== null) {
    deleteItem(itemToDelete);
    dialog.close();
  }
});
```

Change your delete button from `onclick="deleteItem(id)"` to `onclick="showDeleteConfirm(id)"`.

Optional styling:
```css
dialog {
  border: none;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

dialog div {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: flex-end;
}

dialog button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

dialog #cancelBtn {
  background: #e5e7eb;
}

dialog #confirmDeleteBtn {
  background: #dc2626;
  color: white;
}
```

Uses the native `<dialog>` element (no library needed) with `showModal()` to create a modal overlay. The delete only fires when the user clicks Delete, not on Cancel.
