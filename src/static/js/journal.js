function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
    }
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('active');
    }
}

// Abre únicamente la ventana modal del reporte
function abrirModalReporte() {
    abrirModal('modalReportePdf');
}

function cerrarModalReporte() {
    cerrarModal('modalReportePdf');
}

let errorTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
    const formReporte = document.getElementById('formReportePdf');

    if (formReporte) {
        formReporte.addEventListener('submit', (e) => {
            e.preventDefault();

            const startDate = document.getElementById('pdf_start_date');
            const endDate = document.getElementById('pdf_end_date');
            const errorSummary = formReporte.querySelector('.form-error');

            // Limpiar errores previos
            if (errorSummary) {
                errorSummary.textContent = "";
                errorSummary.classList.remove('active');
            }
            if (errorTimeout) clearTimeout(errorTimeout);

            let isFormInvalid = false;

            // Validación de obligatoriedad para ambas fechas
            [startDate, endDate].forEach(control => {
                control.classList.remove('input-error-border');
                if (!control || !control.value.trim()) {
                    isFormInvalid = true;
                    control.classList.add('input-error-border');
                }
            });

            // Si falta alguna fecha, detiene el proceso y muestra alerta
            if (isFormInvalid) {
                if (errorSummary) {
                    errorSummary.textContent = "Por favor, seleccione las fechas 'Desde' y 'Hasta' para generar el reporte.";
                    errorSummary.classList.add('active');
                    errorTimeout = setTimeout(() => {
                        [startDate, endDate].forEach(c => c.classList.remove('input-error-border'));
                        errorSummary.classList.remove('active');
                    }, 4000);
                }
                return; // Detiene la ejecución, impidiendo abrir el PDF
            }

            // Si ambas fechas están seleccionadas, procede a generar el PDF
            const baseUrl = formReporte.getAttribute('action');
            const params = new URLSearchParams();

            params.append('start_date', startDate.value);
            params.append('end_date', endDate.value);

            const finalUrl = `${baseUrl}?${params.toString()}`;

            window.open(finalUrl, '_blank');
            cerrarModalReporte();
        });
    }
});