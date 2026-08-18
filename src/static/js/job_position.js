document.addEventListener('DOMContentLoaded', () => {
    // Modal controls for registration
    const openJobPositionModalBtn = document.getElementById('openJobPositionModalBtn');
    const JobPositionModal = document.getElementById('JobPositionModal');
    const closeJobPositionBtn = document.getElementById('closeJobPositionBtn');
    
    // Form inputs by ID
    const positionInput = document.getElementById('NombrePuestoTrabajo');
    const salaryInput = document.getElementById('Sueldo');
    const updatePositionInput = document.getElementById('UpdateNombrePuestoTrabajo');
    const updateSalaryInput = document.getElementById('UpdateSueldo');

    // Handle open/close modal action
    if (openJobPositionModalBtn && JobPositionModal && closeJobPositionBtn) {
        openJobPositionModalBtn.addEventListener('click', () => {
            const form = JobPositionModal.querySelector('form');
            if (form) form.reset();
            JobPositionModal.classList.add('active');
        });
        closeJobPositionBtn.addEventListener('click', () => JobPositionModal.classList.remove('active'));
    }

    // Direct restrictions for position name inputs (Register)
    if (positionInput) {
        positionInput.maxLength = 50;
        positionInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for position name inputs (Update)
    if (updatePositionInput) {
        updatePositionInput.maxLength = 50;
        updatePositionInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Direct restrictions for salary numeric inputs (Register)
    if (salaryInput) {
        salaryInput.maxLength = 20;
        salaryInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
        });
    }

    // Direct restrictions for salary numeric inputs (Update)
    if (updateSalaryInput) {
        updateSalaryInput.maxLength = 20;
        updateSalaryInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
        });
    }
});

// GLOBAL TABLES FUNCTIONS (PUESTOS DE TRABAJO)

// Open update modal and populate inputs with active row data
function openUpdateModal(id, nombre, sueldo) {
    const UpdateJobPositionModal = document.getElementById('UpdateJobPositionModal');
    const UpdateJobPositionForm = document.getElementById('UpdateJobPositionForm');
    const closeUpdateJobPositionBtn = document.getElementById('closeUpdateJobPositionBtn');
    const UpdateNombrePuestoTrabajo = document.getElementById('UpdateNombrePuestoTrabajo');
    const UpdateSueldo = document.getElementById('UpdateSueldo');

    if (UpdateJobPositionModal && UpdateJobPositionForm && UpdateNombrePuestoTrabajo && UpdateSueldo && closeUpdateJobPositionBtn) {
        UpdateJobPositionForm.action = `/puestos_trabajo/update_job_position/${id}`;
        UpdateNombrePuestoTrabajo.value = nombre;
        UpdateSueldo.value = sueldo;
        UpdateJobPositionModal.classList.add('active');
        
        closeUpdateJobPositionBtn.addEventListener('click', () => UpdateJobPositionModal.classList.remove('active'));
    }
}

// Open delete modal and configure action URL
function openDeleteModal(id) {
    const DeleteJobPositionModal = document.getElementById('DeleteJobPositionModal');
    const DeleteJobPositionForm = document.getElementById('DeleteJobPositionForm');
    const closeDeleteJobPositionBtn = document.getElementById('closeDeleteJobPositionBtn');

    if (DeleteJobPositionModal && DeleteJobPositionForm && closeDeleteJobPositionBtn) {
        DeleteJobPositionForm.action = `/puestos_trabajo/delete_job_position/${id}`;
        DeleteJobPositionModal.classList.add('active'); 
        
        closeDeleteJobPositionBtn.addEventListener('click', () => DeleteJobPositionModal.classList.remove('active'));
    }
}