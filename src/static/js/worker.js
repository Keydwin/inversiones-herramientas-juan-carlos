document.addEventListener('DOMContentLoaded', () => {
    // Modal controls for worker registration
    const openWorkerModalBtn = document.getElementById('openWorkerModalBtn');
    const WorkerModal = document.getElementById('WorkerModal');
    const closeWorkerBtn = document.getElementById('closeWorkerBtn');

    // Registration inputs
    const cedulaInput = document.getElementById('Cedula');
    const nombreInput = document.getElementById('Nombre');
    const apellidoInput = document.getElementById('Apellido');
    const telefonoInput = document.getElementById('Telefono');

    // Update inputs
    const updateCedulaInput = document.getElementById('UpdateCedula');
    const updateNombreInput = document.getElementById('UpdateNombre');
    const updateApellidoInput = document.getElementById('UpdateApellido');
    const updateTelefonoInput = document.getElementById('UpdateTelefono');

    // Handle open/close modal action
    if (openWorkerModalBtn && WorkerModal && closeWorkerBtn) {
        openWorkerModalBtn.addEventListener('click', () => {
            const form = WorkerModal.querySelector('form');
            if (form) form.reset();
            WorkerModal.classList.add('active');
        });
        closeWorkerBtn.addEventListener('click', () => WorkerModal.classList.remove('active'));
    }

    // Direct restrictions for Cédula numeric input (Register)
    if (cedulaInput) {
        cedulaInput.maxLength = 10;
        cedulaInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Direct restrictions for Name text input (Register)
    if (nombreInput) {
        nombreInput.maxLength = 50;
        nombreInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for Last Name text input (Register)
    if (apellidoInput) {
        apellidoInput.maxLength = 50;
        apellidoInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for Phone numeric input (Register)
    if (telefonoInput) {
        telefonoInput.maxLength = 11;
        telefonoInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Direct restrictions for Cédula numeric input (Update)
    if (updateCedulaInput) {
        updateCedulaInput.maxLength = 10;
        updateCedulaInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Direct restrictions for Name text input (Update)
    if (updateNombreInput) {
        updateNombreInput.maxLength = 50;
        updateNombreInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for Last Name text input (Update)
    if (updateApellidoInput) {
        updateApellidoInput.maxLength = 50;
        updateApellidoInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for Phone numeric input (Update)
    if (updateTelefonoInput) {
        updateTelefonoInput.maxLength = 11;
        updateTelefonoInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }
});

// GLOBAL TABLES FUNCTIONS (TRABAJADORES)

// Open update modal and populate input controls
function openUpdateModal(id, cedula, nombre, apellido, telefono, idPuesto) {
    const UpdateWorkerModal = document.getElementById('UpdateWorkerModal');
    const UpdateWorkerForm = document.getElementById('UpdateWorkerForm');
    const closeUpdateWorkerBtn = document.getElementById('closeUpdateWorkerBtn');
    
    const UpdateCedula = document.getElementById('UpdateCedula');
    const UpdateNombre = document.getElementById('UpdateNombre');
    const UpdateApellido = document.getElementById('UpdateApellido');
    const UpdateTelefono = document.getElementById('UpdateTelefono');
    const UpdateIdPuestoTrabajo = document.getElementById('UpdateIdPuestoTrabajo');

    if (UpdateWorkerModal && UpdateWorkerForm && closeUpdateWorkerBtn) {
        UpdateWorkerForm.action = `/trabajadores/update_worker/${id}`;
        
        if (UpdateCedula) UpdateCedula.value = cedula;
        if (UpdateNombre) UpdateNombre.value = nombre;
        if (UpdateApellido) UpdateApellido.value = apellido;
        if (UpdateTelefono) UpdateTelefono.value = telefono;
        if (UpdateIdPuestoTrabajo) UpdateIdPuestoTrabajo.value = idPuesto;

        UpdateWorkerModal.classList.add('active');
        
        closeUpdateWorkerBtn.addEventListener('click', () => UpdateWorkerModal.classList.remove('active'));
    }
}

// Open delete modal and configure action route
function openDeleteModal(id) {
    const DeleteWorkerModal = document.getElementById('DeleteWorkerModal');
    const DeleteWorkerForm = document.getElementById('DeleteWorkerForm');
    const closeDeleteWorkerBtn = document.getElementById('closeDeleteWorkerBtn');

    if (DeleteWorkerModal && DeleteWorkerForm && closeDeleteWorkerBtn) {
        DeleteWorkerForm.action = `/trabajadores/delete_worker/${id}`;
        DeleteWorkerModal.classList.add('active'); 
        
        closeDeleteWorkerBtn.addEventListener('click', () => DeleteWorkerModal.classList.remove('active'));
    }
}