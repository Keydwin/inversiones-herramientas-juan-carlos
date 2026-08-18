document.addEventListener('DOMContentLoaded', () => {
    // --- LÓGICA DEL MODAL DE REGISTRO ---
    const openWorkstationModalBtn = document.getElementById('openWorkstationModalBtn');
    const WorkstationModal = document.getElementById('WorkstationModal');
    const closeWorkstationBtn = document.getElementById('closeWorkstationBtn');
    
    // Inputs para validación
    const nombreInput = document.getElementById('NombrePuestoTrabajo');
    const updateNombreInput = document.getElementById('UpdateNombre');

    if (openWorkstationModalBtn && WorkstationModal && closeWorkstationBtn) {
        openWorkstationModalBtn.addEventListener('click', () => {
            const form = WorkstationModal.querySelector('form');
            if (form) form.reset();
            WorkstationModal.classList.add('active');
        });
        closeWorkstationBtn.addEventListener('click', () => WorkstationModal.classList.remove('active'));
    }

    // --- VALIDACIONES DE TEXTO (Solo letras) ---
    if (nombreInput) {
        nombreInput.maxLength = 25;
        nombreInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    if (updateNombreInput) {
        updateNombreInput.maxLength = 25;
        updateNombreInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // --- LÓGICA PARA OCULTAR LOS MENSAJES FLASH (Igual al video) ---
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0'; // Efecto de desvanecimiento
            setTimeout(() => {
                alert.style.display = 'none'; // Se quita del espacio
            }, 300);
        }, 3000); // Desaparece a los 3 segundos
    });
});


// --- FUNCIONES GLOBALES (MODIFICAR Y ELIMINAR) ---
function openUpdateModal(id, nombre, sueldo) {
    const UpdateWorkstationModal = document.getElementById('UpdateWorkstationModal');
    const UpdateWorkstationForm = document.getElementById('UpdateWorkstationForm');
    const closeUpdateWorkstationBtn = document.getElementById('closeUpdateWorkstationBtn');
    
    const updateNombre = document.getElementById('UpdateNombre');
    const updateSueldo = document.getElementById('UpdateSueldo');

    if (UpdateWorkstationModal && UpdateWorkstationForm && updateNombre && closeUpdateWorkstationBtn) {
        // Enlazar con la ruta exacta de Python
        UpdateWorkstationForm.action = `/workstation/modificar/${id}`;
        
        // Rellenar campos
        updateNombre.value = nombre;
        if (updateSueldo) updateSueldo.value = sueldo;

        UpdateWorkstationModal.classList.add('active');
    }
    
    closeUpdateWorkstationBtn.addEventListener('click', () => UpdateWorkstationModal.classList.remove('active'));
}

function openDeleteModal(id) {
    const DeleteWorkstationModal = document.getElementById('DeleteWorkstationModal');
    const DeleteWorkstationForm = document.getElementById('DeleteWorkstationForm');
    const closeDeleteWorkstationBtn = document.getElementById('closeDeleteWorkstationBtn');
    
    if (DeleteWorkstationModal && DeleteWorkstationForm && closeDeleteWorkstationBtn) {
        // Enlazar con la ruta exacta de Python
        DeleteWorkstationForm.action = `/workstation/eliminar/${id}`;
        
        DeleteWorkstationModal.classList.add('active');   
    }
    
    closeDeleteWorkstationBtn.addEventListener('click', () => DeleteWorkstationModal.classList.remove('active'));
}