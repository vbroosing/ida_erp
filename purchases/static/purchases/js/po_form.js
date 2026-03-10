document.addEventListener("DOMContentLoaded", function() {
    const addLineBtn = document.getElementById('add-line-btn');
    const wrapper = document.getElementById('lines-wrapper');
    const emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;
    // Este input oculto guarda el total de formularios vivos
    const totalFormsInput = document.getElementById('id_lines-TOTAL_FORMS'); 

    addLineBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Obtenemos el número actual de formularios
        let formCount = parseInt(totalFormsInput.value);
        
        // Reemplazamos el marcador genérico '__prefix__' de Django por el índice real (ej: 1, 2, 3...)
        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
        
        // Agregamos la nueva fila al HTML
        wrapper.insertAdjacentHTML('beforeend', newFormHtml);
        
        // Le avisamos a Django que hay un formulario más
        totalFormsInput.value = formCount + 1;
    });

    // Delegación de eventos para borrar líneas (incluso las nuevas)
    wrapper.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-line-btn')) {
            e.preventDefault();
            const row = e.target.closest('.line-form');
            row.remove();
            
            // Nota: En un sistema en producción más avanzado, al borrar se re-indexan los formularios.
            // Por ahora, ocultar/borrar el nodo del DOM es suficiente para crear nuevas OCs.
        }
    });
});