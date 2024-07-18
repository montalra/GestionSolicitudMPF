from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone

class Rol(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'tipo_rol'

    def __str__(self)-> str:
        return '%s  ' % ( self.nombre)


class TipoIdentificacion(models.Model):
    nombre = models.CharField(max_length=20, null= False, unique=True)
    descripcion = models.CharField(max_length=50, null= False)

    class Meta:
        db_table = 'tipoidentificacion'

    def __str__(self)-> str:
        return '%s - %s ' % ( self.nombre, self.descripcion)

    
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellidos, dni, celular, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email es obligatorio')
        email = self.normalize_email(email)
        usuario_rol = Rol.objects.get(nombre='usuario')
        persona = Persona.objects.create(nombre=nombre, apellidos=apellidos, dni=dni, celular=celular)
        user = self.model(email=email, persona=persona, rol=usuario_rol, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellidos, dni, celular, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, nombre, apellidos, dni, celular, password, **extra_fields)


class Persona(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=100, null=False)
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT)
    numero_identidad = models.CharField(max_length=11, null=False)
    celular = models.CharField(max_length=9, null=False)
    
    class Meta:
        db_table = 'persona'

    def __str__(self):
        return '%s - %s - %s' % (self.nombre, self.apellidos, self.numero_identidad)
    
class EstadoSolicitud(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estado_solicitud'

class EstadoReporte(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estado_reporte'


class Usuario(AbstractBaseUser):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['persona', 'rol']

    objects = UsuarioManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuario'


        
class SolicitudMesaParte(models.Model):
    destinatario = models.CharField(max_length=255, null=False)
    descripcion_solicitud = models.TextField(null=False)
    tipo_identificacion_administrador = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, related_name='tipo_identificacion_administrador')
    nombres_administrador = models.CharField(max_length=255, null=False)
    tipo_identificacion_representante = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, related_name='tipo_identificacion_representante', null=True, blank=True)
    nombres_representante = models.CharField(max_length=255, null=True, blank=True)
    tipo_identificacion_tercero = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, related_name='tipo_identificacion_tercero', null=True, blank=True)
    nombre_tercero_representante = models.CharField(max_length=255, null=True, blank=True)
    domicilio_procesal = models.CharField(max_length=255, null=True, blank=True)
    domicilio_real = models.CharField(max_length=255, null=False)
    numero_documento = models.CharField(max_length=20, null=False)
    numero_pago = models.CharField(max_length=20, null=True, blank=True)
    fecha_recibo = models.DateField(null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fundamento_solicitud = models.TextField(null=False)
    descripcion_documento = models.TextField(null=False)
    fecha_solicitud = models.DateField(null=False)    
    telefono = models.CharField(max_length=15, null=False)
    correo_electronico = models.EmailField(max_length=100, null=True)
    comentario = models.TextField(null=True, blank=True)
    estado = models.ForeignKey(EstadoSolicitud, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo_adjunto = models.FileField(upload_to='solicitudes_adjuntos/', null=True, blank=True)

    def __str__(self):
        return f'Solicitud {self.id}'

    class Meta:
        db_table = 'solicitud_mesaparte'

class ReporteIncidente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255,null=False)
    departamento = models.CharField(max_length=255,null=False)
    telefono = models.CharField(max_length=15,null=False)
    tipo_incidente = models.CharField(max_length=50,null=False)
    fecha = models.DateField(null=False)
    hora = models.TimeField(null=False)
    ubicacion = models.CharField(max_length=255,null=False)
    detalles = models.TextField(null=False)
    policia_notificado = models.CharField(max_length=50,null=False)
    causas = models.CharField(max_length=255, blank=True, null=True)
    recomendaciones = models.CharField(max_length=255, blank=True, null=True)
    notas = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to='incidentes/', blank=True, null=True)
    recibido_por = models.CharField(max_length=255, blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=12, unique=True, editable=False)
    estado = models.ForeignKey(EstadoReporte, on_delete=models.RESTRICT)
    
    class Meta:
        db_table = 'reportes'


    def save(self, *args, **kwargs):
        if not self.numero_seguimiento:
            self.numero_seguimiento = self.generate_unique_tracking_number()
        super().save(*args, **kwargs)

    def generate_unique_tracking_number(self):
        current_year = datetime.now().year
        last_report = ReporteIncidente.objects.filter(numero_seguimiento__contains=f"-{current_year}-MPF").order_by('id').last()
        
        if last_report:
            last_number = int(last_report.numero_seguimiento.split('-')[0])
            new_number = f"{last_number + 1:03d}"
        else:
            new_number = "001"
        
        return f"{new_number}-{current_year}-MPF"

    def __str__(self):
        return self.numero_seguimiento