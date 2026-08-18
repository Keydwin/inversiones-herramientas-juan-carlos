// FUNCIÓN CORREGIDA (Recibe los 7 parámetros enviados desde el HTML)
function openUpdateWorkerModal(id, cedula, nombre, apellido, telefono, idPuesto, sueldo) {
    console.log("ID recibido:", id);
    const UpdateWorkerModal = document.getElementById('UpdateWorkerModal');
    const UpdateWorkerForm = document.getElementById('UpdateWorkerForm');
    
    if (UpdateWorkerModal && UpdateWorkerForm) {
        // Asignamos la ruta con el ID correcto
        UpdateWorkerForm.action = `/trabajador/modificar/${id}`;
        
        // Rellenamos los campos (Asegúrate de que estos IDs existan en tu modal HTML)
        document.getElementById('mod_cedula').value = cedula;
        document.getElementById('mod_nombre').value = nombre;
        document.getElementById('mod_apellido').value = apellido;
        document.getElementById('mod_telefono').value = telefono;
        document.getElementById('mod_sueldo').value = sueldo;
        document.getElementById('mod_puesto').value = idPuesto; 
        
        UpdateWorkerModal.classList.add('active');
    }
}