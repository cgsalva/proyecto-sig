// Estado centralizado de la sección de compras
    const CompraState = {
        productoSeleccionado: null,
        detalleCompraData: [],
        debounceTimer: null
    };

    // Selectores del DOM centralizados
    const DOM = {
        buscarProducto: document.getElementById('buscar_producto'),
        resultados: document.getElementById('resultados'),
        codigoInput: document.getElementById('codigo'),
        nombreInput: document.getElementById('nombre'),
        precioVentaInput: document.getElementById('precio'), // Mantenido para referencia visual
        precioCompraInput: document.getElementById('precio_compra'), // ¡Crucial para compras!
        cantidadInput: document.getElementById('cantidad'),
        detalleCompra: document.getElementById('detalle_compra'),
        totalInput: document.getElementById('total'),
        btnAgregar: document.getElementById('btn_agregar'), // ID recomendado para el botón añadir
        btnCompletar: document.getElementById('btn_completar') // ID recomendado para guardar la compra
    };

    // Utilidad para extraer el Token CSRF de Django
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
       Peticiones de Servidor (API)
       ========================================================================== */

    async function fetchProducts(query) {
        if (!query) {
            DOM.resultados.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/productos/autocomplete/?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Error al conectar con el servidor.');
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
            if (!response.ok) throw new Error('Producto no encontrado.');

            CompraState.productoSeleccionado = await response.json();

            // Rellenar formulario
            DOM.codigoInput.value = CompraState.productoSeleccionado.codigo;
            DOM.nombreInput.value = CompraState.productoSeleccionado.nombre;
            DOM.precioVentaInput.value = parseFloat(CompraState.productoSeleccionado.precio).toFixed(2);

            // Enfocar el precio de compra para que el usuario defina el nuevo costo del proveedor
            DOM.precioCompraInput.focus();
        } catch (error) {
            console.error('Error al obtener producto:', error);
            alert('No se encontró ningún producto con el código ingresado.');
            limpiarFormularioProducto();
        }
    }

    // Envío del JSON estructurado de la compra al servidor
    async function completarCompra() {
        if (CompraState.detalleCompraData.length === 0) {
            alert('No hay productos agregados a la orden de compra.');
            return;
        }

        if (!confirm('¿Desea registrar esta orden de compra? El inventario aumentará.')) {
            return;
        }

        const compraPayload = {
            total: calcularTotalCompra(),
            detalle_compra: CompraState.detalleCompraData.map(item => ({
                codigo: item.codigo,
                cantidad: item.cantidad,
                precio_compra: item.precio_compra // Enviamos el costo real de adquisición
            }))
        };

        try {
            DOM.btnCompletar.disabled = true;

            const response = await fetch('/compras/crear/', { // Endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(compraPayload)
            });

            const data = await response.json();

            if (response.ok) {
                alert('Orden de compra registrada e inventario actualizado con éxito.');
                reiniciarCompraVacia();
            } else {
                throw new Error(data.error || 'Error interno al procesar la transacción.');
            }
        } catch (error) {
            console.error('Error en completarCompra:', error);
            alert(`Error al guardar la compra: ${error.message}`);
        } finally {
            DOM.btnCompletar.disabled = false;
        }
    }

    /* ==========================================================================
       Lógica Interna y Renderizado
       ========================================================================== */

    function renderResults(products) {
        DOM.resultados.innerHTML = '';

        if (products.length === 0) {
            DOM.resultados.innerHTML = '<tr><td colspan="4" class="text-muted">No hay coincidencias.</td></tr>';
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
        if (!CompraState.productoSeleccionado) {
            alert('Seleccione un producto antes de agregarlo.');
            return;
        }

        const cantidad = parseInt(DOM.cantidadInput.value);
        const precioCompra = parseFloat(DOM.precioCompraInput.value);

        if (isNaN(cantidad) || cantidad <= 0) {
            alert('Ingrese una cantidad válida y mayor que cero.');
            DOM.cantidadInput.focus();
            return;
        }

        if (isNaN(precioCompra) || precioCompra < 0) {
            alert('Ingrese un precio de compra válido.');
            DOM.precioCompraInput.focus();
            return;
        }

        // CORRECCIÓN: Usamos el precio de compra del formulario, no el precio de venta del producto
        const totalItem = cantidad * precioCompra;

        // Si el producto ya se encuentra en la lista con el MISMO precio de costo, se unifica la cantidad
        const itemExistente = CompraState.detalleCompraData.find(item =>
            item.codigo === CompraState.productoSeleccionado.codigo && item.precio_compra === precioCompra
        );

        if (itemExistente) {
            itemExistente.cantidad += cantidad;
            itemExistente.total = itemExistente.cantidad * precioCompra;
        } else {
            CompraState.detalleCompraData.push({
                codigo: CompraState.productoSeleccionado.codigo,
                nombre: CompraState.productoSeleccionado.nombre,
                precio_compra: precioCompra,
                cantidad: cantidad,
                total: totalItem
            });
        }

        actualizarInterfazCompra();
        limpiarFormularioProducto();
    }

    function calcularTotalCompra() {
        return CompraState.detalleCompraData.reduce((sum, item) => sum + item.total, 0);
    }

    function actualizarInterfazCompra() {
        DOM.detalleCompra.innerHTML = '';

        CompraState.detalleCompraData.forEach((item, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.codigo}</td>
            <td>${item.nombre}</td>
            <td>$${item.precio_compra.toFixed(2)}</td>
            <td>${item.cantidad}</td>
            <td>$${item.total.toFixed(2)}</td>
            <td>
                <button class="btn btn-danger btn-sm btn-eliminar" data-index="${index}">
                    <span class="fas fa-trash"></span>
                </button>
            </td>
        `;
            DOM.detalleCompra.appendChild(tr);
        });

        // CORRECCIÓN: Se recalcula y renderiza el total dinámicamente en cualquier cambio (añadir/eliminar)
        DOM.totalInput.value = calcularTotalCompra().toFixed(2);
    }

    function eliminarProducto(index) {
        CompraState.detalleCompraData.splice(index, 1);
        actualizarInterfazCompra(); // Ejecuta implícitamente la sincronización del total corregida
    }

    function limpiarFormularioProducto() {
        CompraState.productoSeleccionado = null;
        DOM.codigoInput.value = '';
        DOM.nombreInput.value = '';
        DOM.precioVentaInput.value = '0.00';
        DOM.precioCompraInput.value = '';
        DOM.cantidadInput.value = '';
    }

    function reiniciarCompraVacia() {
        CompraState.detalleCompraData = [];
        limpiarFormularioProducto();
        actualizarInterfazCompra();
        DOM.buscarProducto.value = '';
        DOM.resultados.innerHTML = '';
    }

    /* ==========================================================================
       Manejadores de Eventos (Event Listeners Centralizados)
       ========================================================================== */

    // Evento de búsqueda de autocompletado asistido por Debounce
    DOM.buscarProducto.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        clearTimeout(CompraState.debounceTimer);
        CompraState.debounceTimer = setTimeout(() => {
            fetchProducts(query);
        }, 300);
    });

    // Delegación de Eventos en Resultados de Búsqueda (Cero atributos HTML inline)
    DOM.resultados.addEventListener('click', (e) => {
        const targetBoton = e.target.closest('.btn-seleccionar');
        if (targetBoton) {
            const codigo = targetBoton.getAttribute('data-codigo');
            obtenerProducto(codigo);
        }
    });

    // Delegación de Eventos para eliminar filas de la tabla de detalle
    DOM.detalleCompra.addEventListener('click', (e) => {
        const targetBoton = e.target.closest('.btn-eliminar');
        if (targetBoton) {
            const index = parseInt(targetBoton.getAttribute('data-index'));
            eliminarProducto(index);
        }
    });

    // Disparador de búsqueda mediante la tecla Enter
    DOM.codigoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const codigo = DOM.codigoInput.value.trim();
            if (codigo) obtenerProducto(codigo);
        }
    });

    // Escuchas directos para acciones estructurales
    if (DOM.btnAgregar) {
        DOM.btnAgregar.addEventListener('click', agregarProducto);
    }

    if (DOM.btnCompletar) {
        DOM.btnCompletar.addEventListener('click', completarCompra);
    }