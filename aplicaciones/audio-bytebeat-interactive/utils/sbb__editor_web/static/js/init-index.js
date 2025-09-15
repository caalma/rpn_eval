document.addEventListener('DOMContentLoaded', () => {
    // Filtrar archivos en tiempo real
    document.getElementById('filter-input').addEventListener('input', (e) => {
        const filterText = e.target.value.toLowerCase();
        document.querySelectorAll('#file-list li').forEach(item => {
            const fileName = item.dataset.name.toLowerCase();
            if (fileName.includes(filterText)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });

});
