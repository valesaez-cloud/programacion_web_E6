from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    ROL_CHOICES = [
        (1, 'Administrador'),
        (2, 'Editor'),
        (3, 'Vendedor'),
        (4, 'Usuario'),
    ]
    rol = models.IntegerField(choices=ROL_CHOICES, default=4) 
    contrasena = models.CharField( max_length=128)

    def _str_(self):
        return f"{self.nombre} {self.apellidos}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def _str_(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["nombre"]

    def _str_(self):
        return self.nombre


class Juego(models.Model):
    titulo = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="juegos")
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=255, blank=True)  # URL o ruta a imagen

    class Meta:
        ordering = ["titulo"]

    def _str_(self):
        return self.titulo


class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="pedidos")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-fecha"]

    def _str_(self):
        return f"Pedido #{self.id} de {self.usuario}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    juego = models.ForeignKey(Juego, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def _str_(self):
        return f"{self.juego.titulo} x{self.cantidad}"


    #python manage.py makemigrations  
    #python manage.py migrate
 
