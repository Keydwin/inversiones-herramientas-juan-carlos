document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    if (!form) {
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const usuario = document.getElementById('usuario').value.trim();
        const contraseña = document.getElementById('contraseña').value.trim();
        const errorMsg = document.getElementById('errorMsg');

        function mostrarError(texto) {
            errorMsg.textContent = texto;
            errorMsg.style.display = 'block';

            setTimeout(() => {
                errorMsg.textContent = '';
                errorMsg.style.display = 'none';
            }, 5000);
        }

        if (usuario === '' || contraseña === '') {
            mostrarError('Debe llenar todos los campos');
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario, contraseña })
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = '/dashboard';
            } else {
                mostrarError(result.error || 'Usuario o contraseña incorrectos');
            }
        } catch (error) {
            mostrarError('Error de conexión con el servidor');
        }
    });
});
