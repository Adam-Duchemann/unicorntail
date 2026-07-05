Here's the implementation using the native `<dialog>` element:

**HTML:**
```html
<dialog id="deleteDialog">
  <p>This action cannot be undone</p>
  <div>
    <button id="cancelBtn">Cancel</button>
    <button id="confirmDeleteBtn">Delete</button>
  </div>
</dialog>
```

**JavaScript:**
```javascript
let itemToDelete = null;

document.querySelectorAll('[data-delete-btn]').forEach(btn => {
  btn.addEventListener('click', (e) => {
    itemToDelete = e.currentTarget.dataset.id;
    document.getElementById('deleteDialog').showModal();
  });
});

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('deleteDialog').close();
  itemToDelete = null;
});

document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
  deleteItem(itemToDelete);
  document.getElementById('deleteDialog').close();
  itemToDelete = null;
});
```

**CSS:**
```css
#deleteDialog {
  padding: 2rem;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#deleteDialog::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

#deleteDialog div {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

#deleteDialog button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#deleteDialog #cancelBtn {
  background-color: #e5e7eb;
  color: #1f2937;
}

#deleteDialog #confirmDeleteBtn {
  background-color: #ef4444;
  color: white;
}
```

**Usage:** Mark your delete buttons with `data-delete-btn` and `data-id`:
```html
<button data-delete-btn data-id="123">Delete</button>
```

The `<dialog>` element handles the modal behavior and backdrop natively—no custom JavaScript needed for that part.
