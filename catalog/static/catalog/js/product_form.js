document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('dynamic-categories-container');
    const hiddenCategoryInput = document.getElementById('id_category');
    const statusText = document.getElementById('category-status');
    
    // 1. EXTRAEMOS LA URL DESDE EL HTML
    const apiUrl = container.getAttribute('data-api-url');

    async function loadCategories(parentId = null, level = 0) {
        // 2. USAMOS LA URL EXTRAÍDA AQUÍ
        let url = apiUrl;
        if (parentId) {
            url += `?parent_id=${parentId}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();

            const selects = container.querySelectorAll('select');
            selects.forEach(select => {
                if (parseInt(select.dataset.level) >= level) {
                    select.remove();
                }
            });

            if (data.length > 0) {
                statusText.innerText = ""; 
                
                const selectElement = document.createElement('select');
                selectElement.className = 'form-select border-primary shadow-sm';
                selectElement.dataset.level = level; 
                
                const defaultOption = document.createElement('option');
                defaultOption.text = "--- Selecciona una categoría ---";
                defaultOption.value = "";
                selectElement.appendChild(defaultOption);

                data.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id;
                    option.text = cat.name;
                    selectElement.appendChild(option);
                });

                selectElement.addEventListener('change', function() {
                    const selectedId = this.value;
                    if (selectedId) {
                        hiddenCategoryInput.value = selectedId;
                        loadCategories(selectedId, level + 1);
                    } else {
                        loadCategories(parentId, level); 
                        hiddenCategoryInput.value = parentId || ""; 
                    }
                });

                container.appendChild(selectElement);
            } else {
                if(parentId) {
                    statusText.innerHTML = '<span class="text-success">✓ Sub-categoría final alcanzada</span>';
                }
            }
        } catch (error) {
            console.error("Error cargando categorías:", error);
            statusText.innerText = "Error cargando categorías.";
        }
    }

    loadCategories();
});