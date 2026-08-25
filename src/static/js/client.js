document.addEventListener('DOMContentLoaded', () => {

    const clientModal = document.getElementById('ClientModal');
    const openClientModalBtn = document.getElementById('openClientModalBtn');
    const closeClientBtn = document.getElementById('closeClientBtn');

    if (openClientModalBtn && clientModal) {
        openClientModalBtn.addEventListener('click', () => {
            const form = clientModal.querySelector('form');
            if (form) form.reset();
            
            // Restablecer selects dinámicos al abrir
            const munSelect = document.getElementById('IdMunicipio');
            const parrSelect = document.getElementById('IdParroquia');
            if (munSelect) {
                munSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
                munSelect.disabled = true;
            }
            if (parrSelect) {
                parrSelect.innerHTML = '<option value="">Seleccione una parroquia</option>';
                parrSelect.disabled = true;
            }

            clientModal.classList.add('active');
        });
    }

    if (closeClientBtn && clientModal) {
        closeClientBtn.addEventListener('click', () => {
            clientModal.classList.remove('active');
            const form = clientModal.querySelector('form');
            if (form) form.reset();
        });
    }

    const updateClientModal = document.getElementById('UpdateClientModal');
    const closeUpdateClientBtn = document.getElementById('closeUpdateClientBtn');

    if (closeUpdateClientBtn && updateClientModal) {
        closeUpdateClientBtn.addEventListener('click', () => {
            updateClientModal.classList.remove('active');
            const form = updateClientModal.querySelector('form');
            if (form) form.reset();
        });
    }

    const deleteClientModal = document.getElementById('DeleteClientModal');
    const closeDeleteClientBtn = document.getElementById('closeDeleteClientBtn');

    if (closeDeleteClientBtn && deleteClientModal) {
        closeDeleteClientBtn.addEventListener('click', () => {
            deleteClientModal.classList.remove('active');
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === clientModal) {
            clientModal.classList.remove('active');
            const form = clientModal.querySelector('form');
            if (form) form.reset();
        }
        if (e.target === updateClientModal) {
            updateClientModal.classList.remove('active');
            const form = updateClientModal.querySelector('form');
            if (form) form.reset();
        }
        if (e.target === deleteClientModal) {
            deleteClientModal.classList.remove('active');
        }
    });

    // Register

    // Cedula input
    const inputCedula = document.getElementById('Cedula');
    if (inputCedula) {
        inputCedula.maxLength = 9;
        inputCedula.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Nombre input
    const inputNombre = document.getElementById('Nombre');
    if (inputNombre) {
        inputNombre.maxLength = 30;
        inputNombre.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Apellido input
    const inputApellido = document.getElementById('Apellido');
    if (inputApellido) {
        inputApellido.maxLength = 30;
        inputApellido.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Telefono input
    const inputTelefono = document.getElementById('Telefono');
    if (inputTelefono) {
        inputTelefono.maxLength = 11;
        inputTelefono.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Direccion input
    const inputDireccion = document.getElementById('Direccion');
    if (inputDireccion) {
        inputDireccion.maxLength = 100;
        inputDireccion.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 .,()-]/g, '');
        });
    }


    // Update

    // Update Cedula input
    const inputUpdateCedula = document.getElementById('UpdateCedula');
    if (inputUpdateCedula) {
        inputUpdateCedula.maxLength = 9;
        inputUpdateCedula.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Update Nombre input
    const inputUpdateNombre = document.getElementById('UpdateNombre');
    if (inputUpdateNombre) {
        inputUpdateNombre.maxLength = 30;
        inputUpdateNombre.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Update Apellido input
    const inputUpdateApellido = document.getElementById('UpdateApellido');
    if (inputUpdateApellido) {
        inputUpdateApellido.maxLength = 30;
        inputUpdateApellido.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]/g, '');
        });
    }

    // Update Telefono input
    const inputUpdateTelefono = document.getElementById('UpdateTelefono');
    if (inputUpdateTelefono) {
        inputUpdateTelefono.maxLength = 11;
        inputUpdateTelefono.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }

    // Update Direccion input
    const inputUpdateDireccion = document.getElementById('UpdateDireccion');
    if (inputUpdateDireccion) {
        inputUpdateDireccion.maxLength = 100;
        inputUpdateDireccion.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ0-9 .,()-]/g, '');
        });
    }
});

async function cargarMunicipios(idEstado, munSelectId, parrSelectId, targetMunId = null, targetParrId = null) {
    const munSelect = document.getElementById(munSelectId);
    const parrSelect = document.getElementById(parrSelectId);

    if (!munSelect || !parrSelect) return;

    munSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
    parrSelect.innerHTML = '<option value="">Seleccione una parroquia</option>';
    parrSelect.disabled = true;

    if (idEstado) {
        try {
            const response = await fetch(`/get_municipios/${idEstado}`);
            const municipios = await response.json();

            municipios.forEach(m => {
                const isSelected = targetMunId && m.IdMunicipio == targetMunId ? 'selected' : '';
                munSelect.innerHTML += `<option value="${m.IdMunicipio}" ${isSelected}>${m.Municipio}</option>`;
            });

            munSelect.disabled = false;

            if (targetMunId) {
                await cargarParroquias(targetMunId, parrSelectId, targetParrId);
            }
        } catch (error) {
            console.error('Error al cargar municipios:', error);
        }
    } else {
        munSelect.disabled = true;
    }
}

async function cargarParroquias(idMunicipio, parrSelectId, targetParrId = null) {
    const parrSelect = document.getElementById(parrSelectId);

    if (!parrSelect) return;

    parrSelect.innerHTML = '<option value="">Seleccione una parroquia</option>';

    if (idMunicipio) {
        try {
            const response = await fetch(`/get_parroquias/${idMunicipio}`);
            const parroquias = await response.json();

            parroquias.forEach(p => {
                const isSelected = targetParrId && p.IdParroquia == targetParrId ? 'selected' : '';
                parrSelect.innerHTML += `<option value="${p.IdParroquia}" ${isSelected}>${p.Parroquia}</option>`;
            });

            parrSelect.disabled = false;
        } catch (error) {
            console.error('Error al cargar parroquias:', error);
        }
    } else {
        parrSelect.disabled = true;
    }
}

async function openUpdateModal(idCliente, cedula, nombre, apellido, telefono, idParroquia, direccion) {
    const form = document.getElementById('UpdateClientForm');
    const modal = document.getElementById('UpdateClientModal');

    if (form) {
        form.reset(); // Limpia valores residuales antes de cargar los nuevos
        form.action = `/clientes/update_client/${idCliente}`;
    }

    document.getElementById('UpdateCedula').value = cedula;
    document.getElementById('UpdateNombre').value = nombre;
    document.getElementById('UpdateApellido').value = apellido;
    document.getElementById('UpdateTelefono').value = telefono;
    document.getElementById('UpdateDireccion').value = direccion;

    // Resetear selects
    document.getElementById('UpdateIdEstado').value = '';
    document.getElementById('UpdateIdMunicipio').innerHTML = '<option value="">Seleccione un municipio</option>';
    document.getElementById('UpdateIdMunicipio').disabled = true;
    document.getElementById('UpdateIdParroquia').innerHTML = '<option value="">Seleccione una parroquia</option>';
    document.getElementById('UpdateIdParroquia').disabled = true;

    if (idParroquia && idParroquia !== 'None' && idParroquia !== '') {
        try {
            const response = await fetch(`/get_ubicacion_parroquia/${idParroquia}`);
            if (response.ok) {
                const data = await response.json();
                
                const estadoSelect = document.getElementById('UpdateIdEstado');
                if (estadoSelect) {
                    estadoSelect.value = data.IdEstado;
                    await cargarMunicipios(data.IdEstado, 'UpdateIdMunicipio', 'UpdateIdParroquia', data.IdMunicipio, idParroquia);
                }
            }
        } catch (error) {
            console.error('Error al recuperar la ubicación actual:', error);
        }
    }

    if (modal) {
        modal.classList.add('active');
    }
}

function openDeleteModal(idCliente) {
    const form = document.getElementById('DeleteClientForm');
    const modal = document.getElementById('DeleteClientModal');

    if (form) {
        form.action = `/clientes/delete_client/${idCliente}`;
    }

    if (modal) {
        modal.classList.add('active');
    }
}