from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Persona, Usuario, Rol,TipoIdentificacion, SolicitudMesaParte, EstadoSolicitud,ReporteIncidente
from django.core.validators import EmailValidator, RegexValidator,MinLengthValidator, ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



#LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        validators=[EmailValidator(message="Ingrese una dirección de correo electrónico válida.")]
    )
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


#USUARIO
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email',  'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'email': 'Correo Electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        help_texts = {
            'password2': 'Por favor, confirme su contraseña.',
        }

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','readonly': True}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2


#ADMINISTRADOR
class AdministradorForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email',  'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Correo Electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        help_texts = {
            'password2': 'Por favor, confirme su contraseña.',
        }

class AdministradorUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email']  
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','readonly': True}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

#PERSONA
class PersonaForm(forms.ModelForm):
    dni_validator = RegexValidator(
        regex='^[0-9]{8}$',
        message='El DNI contiene 8 números y no letras.',
        code='invalid_dni'
    )
    ruc_validator = RegexValidator(
        regex='^[0-9]{11}$',
        message='El RUC contiene 11 números y no letras.',
        code='invalid_ruc'
    )

    nombre = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombres Completos'
    )
    apellidos = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(8)],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Apellidos Completos'
    )
    tipo_identificacion = forms.ModelChoiceField(
        queryset=TipoIdentificacion.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Identificación'
    )
    numero_identidad = forms.CharField(
        max_length=11,  # Permitir el máximo de 11 caracteres
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Número de Identificación'
    )
    celular = forms.CharField(
        max_length=9,
        validators=[RegexValidator(regex='^[0-9]{9}$')],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Celular'
    )

    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'tipo_identificacion', 'numero_identidad', 'celular']

    def clean_numero_identidad(self):
        tipo_identificacion = self.cleaned_data.get('tipo_identificacion')
        numero_identidad = self.cleaned_data.get('numero_identidad')

  
        if tipo_identificacion:
            if tipo_identificacion.nombre == 'DNI':
         
                self.dni_validator(numero_identidad)
            elif tipo_identificacion.nombre == 'RUC':
              
                self.ruc_validator(numero_identidad)

        return numero_identidad


class PersonaUpdateForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'tipo_identificacion', 'numero_identidad', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'tipo_identificacion': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'numero_identidad': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
        }


#CONTRASEÑA
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 6 :
            raise forms.ValidationError('La nueva contraseña debe tener al menos 6  caracteres.')
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las nuevas contraseñas no coinciden.')
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return old_password
    
#TIPO ROL

class TipoRolForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre.isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras.")
        
        if len(nombre) < 4 or len(nombre) > 30:
            raise forms.ValidationError("El nombre del rol debe tener entre 4 a 30 caracteres.")
        return nombre

    class Meta:
        model = Rol
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'nombre': {
                'unique': "Este nombre de rol ya está en uso. Por favor, ingrese un nuevo nombre.",
            },
        }

#TIPO DUMENTACION

class TipoIdentificacionForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre.isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras.")

        if len(nombre) < 2 or len(nombre) > 20:
            raise forms.ValidationError("El nombre debe tener entre 2 y 20 caracteres.")
        return nombre

    class Meta:
        model = TipoIdentificacion
        fields = ['nombre','descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ESTADO SOLICITUD
class EstadoSolicitudForm(forms.ModelForm):
    class Meta:
        model = EstadoSolicitud
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'nombre': {
                'unique': "Este nombre de estado ya está en uso. Por favor, ingrese un nuevo nombre.",
            },
        }

# SOLICITUD MESA PARTE


class SolicitudMesaParteForm(forms.ModelForm):
    casilla1 = forms.CharField(
        label='1', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'})
    )
    casilla2 = forms.CharField(
        label='2', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla3 = forms.CharField(
        label='3', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla4 = forms.CharField(
        label='4', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla5 = forms.CharField(
        label='5', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla6 = forms.CharField(
        label='6', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla7 = forms.CharField(
        label='7', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    casilla8 = forms.CharField(
        label='8', max_length=100, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}) 
    )

    fecha_recibo = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        help_text='Ingrese una fecha que no sea futura.',
    )
    fecha_solicitud = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly', 'value': timezone.now().strftime('%d/%m/%Y')}),
        help_text='Fecha de hoy.',
    )

    descripcion_solicitud = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 50}),
        min_length=8,
        error_messages={'min_length': 'La descripción de la solicitud debe tener más de 5 caracteres.'}
    )

    class Meta:
        model = SolicitudMesaParte
        fields = ['destinatario', 'descripcion_solicitud', 'tipo_identificacion_administrador', 'nombres_administrador',
                   'tipo_identificacion_representante', 'nombres_representante', 'tipo_identificacion_tercero',
                 'nombre_tercero_representante', 'domicilio_procesal', 'domicilio_real', 'numero_documento',
                   'numero_pago', 'fecha_recibo', 'monto_pago', 'descripcion_documento', 
                'fecha_solicitud', 'telefono', 'correo_electronico', 'comentario', 'archivo_adjunto']
        widgets = {
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion_administrador': forms.Select(attrs={'class': 'form-control'}),
            'nombres_administrador': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion_representante': forms.Select(attrs={'class': 'form-control'}),
            'nombres_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion_tercero': forms.Select(attrs={'class': 'form-control'}),
            'nombre_tercero_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_procesal': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_real': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_documento': forms.Textarea(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control'}),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'destinatario': 'Sr:',
            'descripcion_solicitud': 'Solicito:',
            'tipo_identificacion_administrador': 'Tipo/Nª de documento',
            'nombres_administrador': 'Apellidos y Nombres/denominación o razón social',
            'tipo_identificacion_representante': 'Tipo/Nª de documento',
            'nombres_representante': 'Apellidos y Nombres/denominación o razón social',
            'tipo_identificacion_tercero': 'Tipo/Nª de documento',
            'nombre_tercero_representante': 'Apellidos y Nombres/denominación o razón social',
            'telefono': 'Telefono',
            'correo_electronico': 'Correo Electronico',
            'domicilio_procesal': '1.4.1. Procesal',
            'domicilio_real': '1.4.2. Real',
            'numero_documento': 'N° documento',
            'numero_pago': 'N° Recibo de Pago',
            'fecha_recibo': 'Fecha de Recibo',
            'monto_pago': 'Monto de Pago',
            'descripcion_documento': 'Descripción de la solicitud',
            'archivo_adjunto': 'Archivo Adjunto (Recuerden sin son dos documentos a mas por favor comprimido acepta formato .zip  y .rar)',
        }
    
    def clean_fecha_recibo(self):
        fecha = self.cleaned_data.get('fecha_recibo')
        if fecha and fecha > timezone.now().date():
            raise ValidationError('La fecha del recibo no puede ser una fecha futura.')
        return fecha
    
    def clean_monto_pago(self):
        monto = self.cleaned_data.get('monto_pago')
        if monto is not None and monto <= 0:
            raise ValidationError('El monto de pago debe ser mayor que 0.')
        return monto

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 9:
            raise ValidationError('El número de teléfono debe tener 9 dígitos numéricos.')
        return telefono
    
    def clean_numero_documento(self):
        tipo_identificacion = self.cleaned_data.get('tipo_identificacion_administrador')
        numero_documento = self.cleaned_data.get('numero_documento')
        if tipo_identificacion and numero_documento:
            if tipo_identificacion.nombre == 'DNI' and (len(numero_documento) != 8 or not numero_documento.isdigit()):
                raise ValidationError('El DNI debe tener 8 dígitos numéricos.')
            elif tipo_identificacion.nombre == 'RUC' and (len(numero_documento) != 11 or not numero_documento.isdigit()):
                raise ValidationError('El RUC debe tener 11 dígitos numéricos.')
        return numero_documento
    
    def clean_descripcion_documento(self):
        descripcion_documento = self.cleaned_data.get('descripcion_documento')
        if len(descripcion_documento) < 10:
            raise ValidationError('La descripción del documento debe tener más de 10 caracteres.')
        return descripcion_documento


    def save(self, commit=True):
        solicitud = super().save(commit=False)
        fundamento_solicitud = []
        for i in range(1, 9):
            casilla = self.cleaned_data.get(f'casilla{i}', '')
            if casilla:
                fundamento_solicitud.append(casilla)
        solicitud.fundamento_solicitud = ','.join(fundamento_solicitud)
        if commit:
            solicitud.save()
        return solicitud
    
class SolicitudMesaParteFormAdministrador(forms.ModelForm):

    casilla1 = forms.CharField(
        label='1', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;', 'readonly': 'readonly'})
    )
    casilla2 = forms.CharField(
        label='2', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla3 = forms.CharField(
        label='3', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla4 = forms.CharField(
        label='4', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla5 = forms.CharField(
        label='5', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla6 = forms.CharField(
        label='6', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla7 = forms.CharField(
        label='7', max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    casilla8 = forms.CharField(
        label='8', max_length=100, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'readonly': 'readonly'}) 
    )

    fecha_recibo = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
        required=False,
        help_text='Ingrese una fecha que no sea futura.',
    )
    fecha_solicitud = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly'}),
        help_text='Fecha de hoy.',
    )

    descripcion_solicitud = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 50, 'readonly': 'readonly'}),
    )
     

    class Meta:
        model = SolicitudMesaParte
        fields = ['destinatario', 'descripcion_solicitud', 'tipo_identificacion_administrador', 'nombres_administrador',
                   'tipo_identificacion_representante', 'nombres_representante', 'tipo_identificacion_tercero',
                 'nombre_tercero_representante', 'domicilio_procesal', 'domicilio_real', 'numero_documento',
                   'numero_pago', 'fecha_recibo', 'monto_pago', 'descripcion_documento', 
                'fecha_solicitud', 'telefono', 'correo_electronico', 'comentario', 'archivo_adjunto','estado']
        widgets = {
            'destinatario': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly',}),
            'tipo_identificacion_administrador': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombres_administrador': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly',}),
            'tipo_identificacion_representante': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombres_representante': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'tipo_identificacion_tercero': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombre_tercero_representante': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'domicilio_procesal': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'domicilio_real': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'numero_pago': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'monto_pago': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'descripcion_documento': forms.Textarea(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', }),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'destinatario': 'Sr(a):',
            'descripcion_solicitud': 'Solicito:',
            'tipo_identificacion_administrador': 'Tipo/Nª de documento',
            'nombres_administrador': 'Apellidos y Nombres/denominación o razón social',
            'tipo_identificacion_representante': 'Tipo/Nª de documento',
            'nombres_representante': 'Apellidos y Nombres/denominación o razón social',
            'tipo_identificacion_tercero': 'Tipo/Nª de documento',
            'nombre_tercero_representante': 'Apellidos y Nombres/denominación o razón social',
            'telefono': 'Telefono',
            'correo_electronico': 'Correo Electronico',
            'domicilio_procesal': '1.4.1. Procesal',
            'domicilio_real': '1.4.2. Real',
            'numero_documento': 'N° documento',
            'numero_pago': 'N° Recibo de Pago',
            'fecha_recibo': 'Fecha de Recibo',
            'monto_pago': 'Monto de Pago',
            'descripcion_documento': 'Descripción de la solicitud',
            'estado': 'Estado',
            'archivo_adjunto': 'Archivo Adjunto (Recuerden sin son dos documentos a mas por favor comprimido acepta formato .zip  y .rar)',
        }


class ReporteIncidenteForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly', 'value': timezone.now().strftime('%d/%m/%Y')}),
        help_text='Fecha de hoy.',
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly', 'value': timezone.now().strftime('%H:%M')}),
        help_text='Hora actual.',
    )
    class Meta:
        model = ReporteIncidente
        fields = [
            'nombre', 'departamento', 'telefono', 'tipo_incidente', 'fecha', 'hora', 'ubicacion', 'detalles',
            'policia_notificado', 'causas', 'recomendaciones', 'notas', 'imagen', 'recibido_por'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_incidente': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'policia_notificado': forms.Select(attrs={'class': 'form-control'}),
            'causas': forms.TextInput(attrs={'class': 'form-control'}),
            'recomendaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'recibido_por': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'departamento': 'Departamento',
            'telefono': 'Número de Teléfono',
            'tipo_incidente': 'Tipo de Incidente',
            'ubicacion': 'Ubicación',
            'detalles': 'Detalles del Incidente',
            'policia_notificado': '¿Se Notificó a la Policía?',
            'causas': 'Causas del Incidente',
            'recomendaciones': 'Recomendaciones de Seguimiento',
            'notas': 'Notas Adicionales',
            'imagen': 'Subir Imagen',
            'recibido_por': 'Reporte Recibido Por',
        }

class ReporteIncidenteFormAdministrador(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly', 'value': timezone.now().strftime('%d/%m/%Y')}),
        help_text='Fecha de hoy.',
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'readonly', 'value': timezone.now().strftime('%H:%M')}),
        help_text='Hora actual.',
    )
    class Meta:
        model = ReporteIncidente
        fields = [
            'nombre', 'departamento', 'telefono', 'tipo_incidente', 'fecha', 'hora', 'ubicacion', 'detalles',
            'policia_notificado', 'causas', 'recomendaciones', 'notas', 'imagen','recibido_por','estado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'tipo_incidente': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows':3 , 'readonly': 'readonly'}),
            'policia_notificado': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'causas': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'recomendaciones': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'readonly': 'readonly'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'recibido_por': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'departamento': 'Departamento',
            'telefono': 'Número de Teléfono',
            'tipo_incidente': 'Tipo de Incidente',           
            'ubicacion': 'Ubicación',
            'detalles': 'Detalles del Incidente',
            'policia_notificado': '¿Se Notificó a la Policía?',
            'causas': 'Causas del Incidente',
            'recomendaciones': 'Recomendaciones de Seguimiento',
            'notas': 'Notas Adicionales',
            'imagen': 'Subir Imagen',
            'recibido_por': 'Reporte Recibido Por',
            'estado': 'Estado',
        }