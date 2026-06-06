from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos"
    )

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    nombre_corto = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Cuenta(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    TIPO_CHOICES = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('patrimonio', 'Patrimonio'),
        ('ingreso', 'Ingreso'),
        ('costos', 'Costos'),
        ('gasto', 'Gasto'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

# ASIENTOS CONTABLES

class AsientoContable(models.Model):
    fecha = models.DateField()
    descripcion = models.TextField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f"Asiento #{self.id}"

    @property
    def total_debe(self):
        return sum(
            (detalle.debe for detalle in self.detalles.all()),
            Decimal('0.00')
        )

    @property
    def total_haber(self):
        return sum(
            (detalle.haber for detalle in self.detalles.all()),
            Decimal('0.00')
        )

    @property
    def balanceado(self):
        return self.total_debe == self.total_haber


class MovimientoContable(models.Model):
    asiento = models.ForeignKey(
        AsientoContable,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )

    debe = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    haber = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.cuenta.nombre}"

# =========================
# COMPRAS
# =========================

class Compra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)

    costo_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Compra #{self.id}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalle_compras'
    )

    costo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cantidad = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.costo_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.codigo} - {self.producto.nombre}"


class Venta(models.Model):

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ventas'
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ventas',
        null=True,
        blank=True
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Venta #{self.id}"


class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalle_ventas'
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.codigo} - {self.producto.nombre}"