document.addEventListener('DOMContentLoaded', () => {
    const itemsContainer = document.getElementById('items');

    // Guardar datos
    document.getElementById('save').addEventListener('click', async () => {
        const items = [];
        document.querySelectorAll('#items tr').forEach(row => {
            items.push({
                data: row.querySelector('.data').value,
                elapsed_time: parseFloat(row.querySelector('.elapsed-time').value)
            });
        });
        const filename = document.getElementById('filename').value;
        await fetch(`/update/${filename}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(items)
        });
        alert('Guardado exitosamente');
    });

    // Agregar nuevo ítem
    document.getElementById('add').addEventListener('click', () => {
        const newRow = document.createElement('tr');
        const idx = itemsContainer.children.length + 1;
        newRow.classList.add('item');
        newRow.setAttribute('draggable', 'true');
        newRow.setAttribute('data-index', idx);
        newRow.innerHTML = `
            <td><p class="small text-center">${idx}</p></td>
            <td><input type="text" class="form-control data" value=""></td>
            <td><input type="number" class="form-control elapsed-time" value="0"></td>
            <td class="actions">
                <span class="btn btn-sm btn-dark"><input type="checkbox" class="select-item" title="Seleccionar"></span>
                <button class="btn btn-sm btn-dark delete" title="Eliminar">🗑</button>
                <button class="btn btn-sm btn-dark listen" data-state="listen" title="Escuchar/Detener audio">▶</button>
            </td>
        `;
        itemsContainer.appendChild(newRow);
        attachRowListeners(newRow);
    });

    let currentListenButton = null;

    // Adjuntar listeners a las filas existentes
    document.querySelectorAll('.item').forEach(row => attachRowListeners(row));

    // Función para adjuntar listeners a una fila
    function attachRowListeners(row) {
        // Escuchar/Detener ítem
        const listenButton = row.querySelector('.listen');
        listenButton.addEventListener('click', async () => {
            const state = listenButton.dataset.state;
            const expression = row.querySelector('.data').value;

            if (state === 'listen') {
                // Cambiar el botón a "Detener"
                listenButton.textContent = '⏹️';
                listenButton.classList.remove('btn-success');
                listenButton.classList.add('btn-danger');
                listenButton.dataset.state = 'stop';

                // Guardar la referencia al botón actual
                currentListenButton = listenButton;

                try {
                    await fetch('/listen', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ expression })
                    });
                } catch (e) {
                    alert('Error al reproducir');
                    resetListenButton(listenButton);
                }
            } else if (state === 'stop') {
                // Cambiar el botón a "Escuchar"
                resetListenButton(listenButton);

                try {
                    await fetch('/listen_stop', {
                        method: 'POST'
                    });
                } catch (e) {
                    alert('Error al detener');
                }
            }
        });

        // Eliminar ítem
        row.querySelector('.delete').addEventListener('click', () => {
            row.remove();
            renumberItems();
        });

        // Resaltar ítems seleccionados
        const checkbox = row.querySelector('.select-item');
        checkbox.addEventListener('input', () => {
            if (checkbox.checked) {
                row.classList.add('selected');
            } else {
                row.classList.remove('selected');
            }
        });

        // Drag and Drop
        row.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', row.dataset.index);
            row.classList.add('dragging');
        });

        row.addEventListener('dragend', () => {
            row.classList.remove('dragging');
            renumberItems();
        });
    }

    // Función para restablecer el botón a "Escuchar"
    function resetListenButton(button) {
        button.textContent = '▶';
        button.classList.remove('btn-danger');
        button.classList.add('btn-success');
        button.dataset.state = 'listen';
    }

    // Renumerar los ítems
    function renumberItems() {
        document.querySelectorAll('#items tr').forEach((row, index) => {
            row.querySelector('td:first-child p').textContent = index + 1;
        });
    }

    // Acciones masivas
    document.getElementById('mass-delete').addEventListener('click', () => {
        document.querySelectorAll('.select-item:checked').forEach(checkbox => {
            checkbox.closest('.item').remove();
        });
        renumberItems();
    });

    document.getElementById('mass-update-time').addEventListener('click', () => {
        const expression = prompt('Ingrese una expresión (ejemplo: * 2, + 10):');
        if (!expression) return;

        document.querySelectorAll('.select-item:checked').forEach(checkbox => {
            const row = checkbox.closest('.item');
            const input = row.querySelector('.elapsed-time');
            let newValue = parseFloat(input.value);

            try {
                if (expression.startsWith('*')) {
                    newValue *= parseFloat(expression.slice(1));
                } else if (expression.startsWith('/')) {
                    newValue /= parseFloat(expression.slice(1));
                } else if (expression.startsWith('+')) {
                    newValue += parseFloat(expression.slice(1));
                } else if (expression.startsWith('-')) {
                    newValue -= parseFloat(expression.slice(1));
                } else {
                    newValue = parseFloat(expression); // Reemplazar con un valor fijo
                }
                input.value = newValue;
            } catch (e) {
                alert('Expresión inválida');
            }
        });
    });

    // Deseleccionar todos
    document.getElementById('deselect-all').addEventListener('click', () => {
        document.querySelectorAll('.select-item').forEach(checkbox => {
            checkbox.checked = false;
            const row = checkbox.closest('.item');
            row.classList.remove('selected');
        });
    });

    // Seleccionar todos
    document.getElementById('select-all').addEventListener('click', () => {
        document.querySelectorAll('.select-item').forEach(checkbox => {
            checkbox.checked = true;
            const row = checkbox.closest('.item');
            row.classList.add('selected');
        });
    });

    // Invertir selección
    document.getElementById('invert-selection').addEventListener('click', () => {
        document.querySelectorAll('.select-item').forEach(checkbox => {
            checkbox.checked = !checkbox.checked;
            const row = checkbox.closest('.item');
            if (checkbox.checked) {
                row.classList.add('selected');
            } else {
                row.classList.remove('selected');
            }
        });
    });

    // Resaltar ítems seleccionados
    document.querySelectorAll('.select-item').forEach(checkbox => {
        checkbox.addEventListener('input', () => {
            const row = checkbox.closest('.item');
            if (checkbox.checked) {
                row.classList.add('selected');
            } else {
                row.classList.remove('selected');
            }
        });
    });


    // Habilitar el arrastre de filas
    document.querySelectorAll('.item').forEach(row => {
        row.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', row.dataset.index);
            row.classList.add('dragging');
        });

        row.addEventListener('dragend', () => {
            row.classList.remove('dragging');
            renumberItems();
        });
    });

    // Manejar el evento de soltar
    document.getElementById('items').addEventListener('dragover', (e) => {
        e.preventDefault(); // Permitir el drop
    });

    document.getElementById('items').addEventListener('drop', (e) => {
        e.preventDefault();
        const draggedIndex = e.dataTransfer.getData('text/plain');
        const draggedRow = document.querySelector(`[data-index="${draggedIndex}"]`);
        const targetRow = e.target.closest('.item');

        if (targetRow && draggedRow !== targetRow) {
            const itemsContainer = document.getElementById('items');
            if (draggedRow.compareDocumentPosition(targetRow) & Node.DOCUMENT_POSITION_FOLLOWING) {
                itemsContainer.insertBefore(draggedRow, targetRow.nextSibling);
            } else {
                itemsContainer.insertBefore(draggedRow, targetRow);
            }
        }
    });
});
