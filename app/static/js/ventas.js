// Usamos un objeto para mantener el estado de la aplicación limpio y centralizado
const AppState = {
    productoSeleccionado: null,
    detalleVentaData: [],
    debounceTimer: null
};

// Selectores del DOM
const DOM = {
    buscarProducto: document.getElementById('buscar_producto'),
    resultados: document.getElementById('resultados'),
    codigoInput: document.getElementById('codigo'),
    nombreInput: document.getElementById('nombre'),
    precioInput: document.getElementById('precio'),
    cantidadInput: document.getElementById('cantidad'),
    detalleVenta: document.getElementById('detalle_venta'),
    totalInput: document.getElementById('total'),
    btnAgregar: document.getElementById('btn_agregar'),
    btnCompletar: document.getElementById('btn_completar')
};

// Auxiliar para obtener el token CSRF de Django de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* ==========================================================================
   Módulos de API (Fetch)
   ========================================================================== */

async function fetchProducts(query) {
    if (!query) {
        DOM.resultados.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/productos/autocomplete/?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Error en la red');
        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error('Error al buscar productos:', error);
        DOM.resultados.innerHTML = '<tr><td colspan="4" class="text-danger">Error al cargar resultados.</td></tr>';
    }
}

async function obtenerProducto(codigo) {
    try {
        const response = await fetch(`/productos/obtener/${codigo}/`);
        if (!response.ok) throw new Error('Producto no encontrado');
        
        AppState.productoSeleccionado = await response.json();
        
        DOM.codigoInput.value = AppState.productoSeleccionado.codigo;
        DOM.nombreInput.value = AppState.productoSeleccionado.nombre;
        DOM.precioInput.value = parseFloat(AppState.productoSeleccionado.precio).toFixed(2);
        DOM.cantidadInput.focus();
    } catch (error) {
        console.error('Error al obtener producto:', error);
        alert('No se encontró ningún producto con ese código.');
        limpiarFormularioProducto();
    }
}

// Enviar la venta al backend
async function completarVenta() {
    if (AppState.detalleVentaData.length === 0) {
        alert('No hay productos en el detalle para procesar la venta.');
        return;
    }

    if (!confirm('¿Está seguro de que desea finalizar esta venta?')) {
        return;
    }

    // Estructura de datos a enviar
    const ventaData = {
        total: calcularTotalVenta(),
        items: AppState.detalleVentaData.map(item => ({
            codigo: item.codigo,
            cantidad: item.cantidad,
            precio: item.precio // Enviamos el precio por si hay cambios de tarifa concurrentes
        }))
    };

    try {
        DOM.btnCompletar.disabled = true; // Evitar doble submit
        
        const response = await fetch('/ventas/crear/', { // Endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Seguridad para Django
            },
            body: JSON.stringify(ventaData)
        });

        const resultado = await response.json();

        if (response.ok) {
            alert('Venta procesada con éxito.');
            reiniciarVentaVacia();
        } else {
            throw new Error(resultado.error || 'Error desconocido al procesar la venta.');
        }
    } catch (error) {
        console.error('Error en completarVenta:', error);
        alert(`Error al procesar la venta: ${error.message}`);
    } finally {
        DOM.btnCompletar.disabled = false;
    }
}

/* ==========================================================================
   Lógica de Negocio y Renderizado
   ========================================================================== */

function renderResults(products) {
    DOM.resultados.innerHTML = '';

    if (products.length === 0) {
        DOM.resultados.innerHTML = '<tr><td colspan="4">No se encontraron coincidencias.</td></tr>';
        return;
    }

    products.forEach(product => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${product.nombre}</td>
            <td>$${parseFloat(product.precio).toFixed(2)}</td>
            <td>${product.stock_actual}</td>
            <td>
                <button class="btn btn-success btn-sm btn-seleccionar" data-codigo="${product.codigo}" data-dismiss="modal" aria-label="Close">
                    <span class="fas fa-plus"></span>
                </button>
            </td>
        `;
        DOM.resultados.appendChild(tr);
    });
}

function agregarProducto() {
    if (!AppState.productoSeleccionado) {
        alert('Por favor, selecciona o busca un producto primero.');
        return;
    }

    const cantidad = parseInt(DOM.cantidadInput.value);
    if (isNaN(cantidad) || cantidad <= 0) {
        alert('Por favor, ingresa una cantidad válida mayor a cero.');
        DOM.cantidadInput.focus();
        return;
    }

    // Verificar si el producto ya existe en el detalle para acumularlo
    const itemExistente = AppState.detalleVentaData.find(item => item.codigo === AppState.productoSeleccionado.codigo);
    const precio = parseFloat(AppState.productoSeleccionado.precio);

    if (itemExistente) {
        itemExistente.cantidad += cantidad;
        itemExistente.total = itemExistente.cantidad * precio;
    } else {
        AppState.detalleVentaData.push({
            codigo: AppState.productoSeleccionado.codigo,
            nombre: AppState.productoSeleccionado.nombre,
            precio: precio,
            cantidad: cantidad,
            total: cantidad * precio
        });
    }

    actualizarInterfazVenta();
    limpiarFormularioProducto();
}

function calcularTotalVenta() {
    return AppState.detalleVentaData.reduce((sum, item) => sum + item.total, 0);
}

function actualizarInterfazVenta() {
    DOM.detalleVenta.innerHTML = '';
    
    AppState.detalleVentaData.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.codigo}</td>
            <td>${item.nombre}</td>
            <td>$${item.precio.toFixed(2)}</td>
            <td>${item.cantidad}</td>
            <td>$${item.total.toFixed(2)}</td>
            <td>
                <button class="btn btn-danger btn-sm btn-eliminar" data-index="${index}">
                    <span class="fas fa-trash"></span>
                </button>
            </td>
        `;
        DOM.detalleVenta.appendChild(tr);
    });

    // Actualizar el input del Total
    DOM.totalInput.value = calcularTotalVenta().toFixed(2);
}

function eliminarProducto(index) {
    AppState.detalleVentaData.splice(index, 1);
    actualizarInterfazVenta();
}

function limpiarFormularioProducto() {
    AppState.productoSeleccionado = null;
    DOM.codigoInput.value = '';
    DOM.nombreInput.value = '';
    DOM.precioInput.value = '0.00';
    DOM.cantidadInput.value = '';
}

function reiniciarVentaVacia() {
    AppState.detalleVentaData = [];
    limpiarFormularioProducto();
    actualizarInterfazVenta();
    DOM.buscarProducto.value = '';
    DOM.resultados.innerHTML = '';
}

/* ==========================================================================
   Listeners de Eventos
   ========================================================================== */

// Debounce para la barra de búsqueda
DOM.buscarProducto.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(AppState.debounceTimer);
    AppState.debounceTimer = setTimeout(() => {
        fetchProducts(query);
    }, 300);
});

// Event Delegation para la tabla de resultados de búsqueda
DOM.resultados.addEventListener('click', (e) => {
    const boton = e.target.closest('.btn-seleccionar');
    if (boton) {
        const codigo = boton.getAttribute('data-codigo');
        obtenerProducto(codigo);
    }
});

// Event Delegation para la tabla de detalle de ventas
DOM.detalleVenta.addEventListener('click', (e) => {
    const boton = e.target.closest('.btn-eliminar');
    if (boton) {
        const index = parseInt(boton.getAttribute('data-index'));
        eliminarProducto(index);
    }
});

// Buscar por código con Enter
DOM.codigoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        const codigo = DOM.codigoInput.value.trim();
        if (codigo) obtenerProducto(codigo);
    }
});

// Listener para el botón manual de Agregar
if (DOM.btnAgregar) {
    DOM.btnAgregar.addEventListener('click', agregarProducto);
}

// Listener para completar Venta
if (DOM.btnCompletar) {
    DOM.btnCompletar.addEventListener('click', completarVenta);
}
