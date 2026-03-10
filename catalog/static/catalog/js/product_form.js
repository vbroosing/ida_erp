document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('dynamic-categories-container');
    const hiddenCategoryInput = document.getElementById('id_category'); // Django nombra los inputs como id_NOMBREDELCAMPO
    const statusText = document.getElementById('category-status');

    // Función principal para buscar y pintar categorías
    async function loadCategories(parentId = null, level = 0) {
        // Construimos la URL
        let url = "{% url 'api_subcategories' %}";
        if (parentId) {
            url += `?parent_id=${parentId}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();

            // Borramos los selects que estén por debajo del nivel actual
            // (por si el usuario se arrepiente y cambia una categoría más arriba)
            const selects = container.querySelectorAll('select');
            selects.forEach(select => {
                if (parseInt(select.dataset.level) >= level) {
                    select.remove();
                }
            });

            if (data.length > 0) {
                statusText.innerText = ""; // Limpiar mensaje
                
                // Crear nuevo select
                const selectElement = document.createElement('select');
                selectElement.className = 'form-select border-primary shadow-sm';
                selectElement.dataset.level = level; // Guardamos el nivel de profundidad
                
                // Opción por defecto
                const defaultOption = document.createElement('option');
                defaultOption.text = "--- Selecciona una categoría ---";
                defaultOption.value = "";
                selectElement.appendChild(defaultOption);

                // Llenar con opciones de la API
                data.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.id;
                    option.text = cat.name;
                    selectElement.appendChild(option);
                });

                // Escuchar cuando el usuario elija una opción
                selectElement.addEventListener('change', function() {
                    const selectedId = this.value;
                    if (selectedId) {
                        // Actualizar el input oculto de Django con la elección actual
                        hiddenCategoryInput.value = selectedId;
                        // Cargar el siguiente nivel (hijos)
                        loadCategories(selectedId, level + 1);
                    } else {
                        // Si vuelve a "---", limpiar los de abajo
                        loadCategories(parentId, level); // Recargar este nivel para borrar los hijos
                        // Si hay un nivel anterior, asignar ese ID, si no, limpiar
                        hiddenCategoryInput.value = parentId || ""; 
                    }
                });

                container.appendChild(selectElement);
            } else {
                // Si la API devuelve 0 resultados, significa que llegamos al final del árbol
                if(parentId) {
                    statusText.innerHTML = '<span class="text-success">✓ Sub-categoría final alcanzada</span>';
                }
            }
        } catch (error) {
            console.error("Error cargando categorías:", error);
            statusText.innerText = "Error cargando categorías.";
        }
    }

    // Inicializar cargando las categorías raíz (Nivel 0)
    loadCategories();
});