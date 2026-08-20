document.addEventListener('DOMContentLoaded', () => {
    const openUserModalBtn = document.getElementById('openUserModalBtn');
    const UserModal = document.getElementById('UserModal');
    const closeUserBtn = document.getElementById('closeUserBtn');
    const userInput = document.getElementById('NombreUsuario');
    const UpdateUser = document.getElementById('UpdateNombreUsuario');

    if (openUserModalBtn && UserModal && closeUserBtn) {
        openUserModalBtn.addEventListener('click', () => {
            const form = UserModal.querySelector('form');
            if (form) form.reset();
            UserModal.classList.add('active');
        });
        closeUserBtn.addEventListener('click', () => UserModal.classList.remove('active'));
    }

    if (userInput) {
        userInput.maxLength = 25;
        userInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-Z0-9_.]/g, '');
        });
    }

    if (UpdateUser) {
        UpdateUser.maxLength = 25;
        UpdateUser.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^a-zA-Z0-9_.]/g, '');
        });
    }
});

function openUpdateModal(id, nombre, idTrabajador, password) {
    const UpdateUserModal = document.getElementById('UpdateUserModal');
    const UpdateUserForm = document.getElementById('UpdateUserForm');
    const closeUpdateUserBtn = document.getElementById('closeUpdateUserBtn');
    const UpdateNombreUsuario = document.getElementById('UpdateNombreUsuario');
    const UpdateIdTrabajador = document.getElementById('UpdateIdTrabajador');
    const UpdatePassword = document.getElementById('UpdatePassword');

    if (UpdateUserModal && UpdateUserForm && UpdateNombreUsuario && closeUpdateUserBtn) {
        UpdateUserForm.action = `/usuarios/update_user/${id}`;
        UpdateNombreUsuario.value = nombre;
        if (UpdatePassword) UpdatePassword.value = password;


        if (UpdateIdTrabajador) {
            Array.from(UpdateIdTrabajador.options).forEach(option => {
                const esElActual = option.value === String(idTrabajador);
                const estaOcupado = option.getAttribute('data-ocupado') === 'true';


                if (esElActual || !estaOcupado) {
                    option.style.display = '';
                    option.disabled = false;
                } else {
                    option.style.display = 'none';
                    option.disabled = true;
                }
            });
            UpdateIdTrabajador.value = idTrabajador;
        }

        UpdateUserModal.classList.add('active');
    }
    closeUpdateUserBtn.addEventListener('click', () => UpdateUserModal.classList.remove('active'));
}

function openDeleteModal(id) {
    const DeleteUserModal = document.getElementById('DeleteUserModal');
    const DeleteUserForm = document.getElementById('DeleteUserForm');
    const closeDeleteUserBtn = document.getElementById('closeDeleteUserBtn');

    if (DeleteUserModal && DeleteUserForm) {
        DeleteUserForm.action = `/usuarios/delete_user/${id}`;
        DeleteUserModal.classList.add('active');   
    }
    closeDeleteUserBtn.addEventListener('click', () => DeleteUserModal.classList.remove('active'));
}