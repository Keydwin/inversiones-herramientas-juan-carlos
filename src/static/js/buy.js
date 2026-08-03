// Las funciones deben ser globales para que el 'onclick' del HTML pueda llamarlas
function abrirModalDetalle(idCompra) {
    const modal = document.getElementById(`modalDetalle${idCompra}`);
    if (modal) {
        modal.classList.add("active");
    }
}

function cerrarModalDetalle(idCompra) {
    const modal = document.getElementById(`modalDetalle${idCompra}`);
    if (modal) {
        modal.classList.remove("active");
    }
}

