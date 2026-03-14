document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('dynamic-parent-container');
    // ATENCIÓN AQUÍ: Buscamos el input 'id_parent' que genera Django para el campo parent
    const hiddenParentInput = document.getElementById('id_parent'); 
    const statusText = document.getElementById('parent-status');
    
    const apiUrl = container.getAttribute('data-api-url');

    async function loadCategories(parentId = null, level = 0) {
        let url = apiUrl;
        if (parentId) {
            url += `?parent_id=${parentId}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();

            // Limpiamos los niveles inferiores si el usuario cambia de opinión
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
                // Texto dinámico para ayudar al usuario
                defaultOption.text = level === 0 ? "--- Sin categoría padre (Será una categoría raíz) ---" : "--- Selecciona una sub-categoría ---";
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
                        hiddenParentInput.value = selectedId;
                        loadCategories(selectedId, level + 1);
                    } else {
                        loadCategories(parentId, level); 
                        // Si retrocede a "---", toma el ID del nivel anterior, o queda vacío si es la raíz
                        hiddenParentInput.value = parentId || ""; 
                    }
                });

                container.appendChild(selectElement);
            } else {
                // Llegó al final del árbol
                if(parentId) {
                    statusText.innerHTML = '<span class="text-success">✓ La nueva categoría se creará dentro de esta selección.</span>';
                }
            }
        } catch (error) {
            console.error("Error cargando categorías:", error);
            statusText.innerText = "Error cargando categorías.";
        }
    }

    // Arrancamos buscando las categorías raíz
    loadCategories();
});