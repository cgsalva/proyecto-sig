
const tablaMovimientos = document.getElementById('tabla-movimientos')
const btnAgregarFila = document.getElementById('agregar-fila')

function calcularTotales() {

    let totalDebe = 0
    let totalHaber = 0

    document.querySelectorAll('.debe').forEach(input => {
        totalDebe += parseFloat(input.value || 0)
    })

    document.querySelectorAll('.haber').forEach(input => {
        totalHaber += parseFloat(input.value || 0)
    })

    document.getElementById('total-debe').textContent =
        totalDebe.toFixed(2)

    document.getElementById('total-haber').textContent =
        totalHaber.toFixed(2)

    const estado = document.getElementById('estado-balance')

    if (totalDebe === totalHaber && totalDebe > 0) {

        estado.classList.remove('alert-warning')
        estado.classList.add('alert-success')

        estado.textContent = 'El asiento está balanceado'

    } else {

        estado.classList.remove('alert-success')
        estado.classList.add('alert-warning')

        estado.textContent =
            'El asiento no está balanceado'
    }
}

btnAgregarFila.addEventListener('click', () => {

    const fila = `
        <tr>

            <td>

                <select
                    name="cuenta[]"
                    class="form-control form-control-sm"
                    required
                >

                    <option value="">
                        Seleccionar cuenta
                    </option>

                    {% for cuenta in cuentas %}

                        <option value="{{ cuenta.codigo }}">
                            {{ cuenta.codigo }} - {{ cuenta.nombre }}
                        </option>

                    {% endfor %}

                </select>

            </td>

            <td>

                <input
                    type="number"
                    step="0.01"
                    min="0"
                    name="debe[]"
                    class="form-control form-control-sm debe"
                    value="0"
                    required
                >

            </td>

            <td>

                <input
                    type="number"
                    step="0.01"
                    min="0"
                    name="haber[]"
                    class="form-control form-control-sm haber"
                    value="0"
                    required
                >

            </td>

            <td class="text-center">

                <button
                    type="button"
                    class="btn btn-danger btn-sm eliminar-fila"
                >
                    <i class="fa-solid fa-trash-can"></i>
                </button>

            </td>

        </tr>
    `

    tablaMovimientos.insertAdjacentHTML(
        'beforeend',
        fila
    )

})

document.addEventListener('input', calcularTotales)

document.addEventListener('click', function (event) {

    if (event.target.classList.contains('eliminar-fila')) {

        event.target.closest('tr').remove()

        calcularTotales()
    }

})

calcularTotales()
