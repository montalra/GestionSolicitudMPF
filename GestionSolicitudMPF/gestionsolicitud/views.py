from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponse
import os
from .forms import UsuarioForm, AdministradorForm, PersonaForm,LoginForm,UsuarioUpdateForm, PersonaUpdateForm,AdministradorUpdateForm,CustomPasswordChangeForm
from .forms import TipoRolForm,TipoIdentificacionForm,EstadoSolicitudForm,SolicitudMesaParteForm,SolicitudMesaParteFormAdministrador,ReporteIncidenteForm,ReporteIncidenteFormAdministrador
from django.contrib import messages
from .models import Rol, Usuario,TipoIdentificacion,EstadoSolicitud,SolicitudMesaParte,ReporteIncidente,EstadoReporte
from .decorators import role_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

#Login
def login_user(request):
    next_url = request.GET.get('next')  
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                elif user.rol.nombre == 'Usuario':
                    return redirect('menu_principal')
                elif user.rol.nombre == 'Administrador':
                    return redirect('panel_control')
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
        else:
            messages.error(request, 'Invalid Form Submission', extra_tags='login')
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

#Errore
def error_403(request):
    return render(request, 'errors/403.html')

def error_404(request ):
    return render(request, 'errors/404.html', status=404)

#Terminos y condiciones
def Terminosycondiciones(request):
   return render(request, 'terminosycodiciones/terminoycondiciones.html')

#Menu Principal

@login_required
@role_required('Usuario')
def menuPrincipal(request):
    return render(request, 'menuusuario/menuusuario.html')

#Menu administrador
@login_required
@role_required('Administrador')
def menuControl(request):
    return render(request, 'menuadministrador/menuadministrador.html')



#USUARIO
@login_required
@role_required('Administrador')
def UsuarioLista(request):
    usuarios = Usuario.objects.filter(rol__nombre='usuario')
    return render(request, 'usuario/listar_usuario.html', {'object_list': usuarios})

def UsuarioRegistro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        persona_form = PersonaForm(request.POST)
        if usuario_form.is_valid() and persona_form.is_valid():
            persona = persona_form.save()
            user = usuario_form.save(commit=False)
            user.persona = persona
            user.rol = Rol.objects.get(nombre='usuario') 
            user.save()
            login(request, user)
            return redirect('login')
    else:
        usuario_form = UsuarioForm()
        persona_form = PersonaForm()
    return render(request, 'usuario/nuevo_usuario.html', {'usuario_form': usuario_form, 'persona_form': persona_form})


@login_required
@role_required('Usuario')
def UsuarioActualizar(request, usuario_id):
    try:
        usuario = get_object_or_404(Usuario, id=usuario_id)
        if request.user != usuario:
            return redirect('error_403')
        if request.method == 'POST':
           usuario_form = UsuarioUpdateForm(request.POST, instance=usuario)
           persona_form = PersonaUpdateForm(request.POST, instance=usuario.persona)
           password_change_form = CustomPasswordChangeForm(request.user, request.POST)
           if usuario_form.is_valid() and persona_form.is_valid() and password_change_form.is_valid():
               usuario_form.save()
               persona_form.save()
               password_change_form.save()
               messages.success(request, 'Usuario actualizado exitosamente.')
               return redirect('actualizar_usuario', usuario_id=usuario.id)
        else:
            usuario_form = UsuarioUpdateForm(instance=usuario)
            persona_form = PersonaUpdateForm(instance=usuario.persona)
            password_change_form = CustomPasswordChangeForm(request.user)
        return render(request, 'usuario/actualizar_usuario.html', {'usuario_form': usuario_form, 'persona_form': persona_form, 'password_change_form': password_change_form})
    except Http404:
        return render(request, 'errors/404.html', status=404)


@login_required
@role_required('Administrador')
def UsuarioEliminar(request, usuario_id):
    if not request.user.is_staff:
        return redirect('error_403')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('usuario_lista')
    return render(request, 'usuario/eliminar_usuario.html', {'usuario': usuario})




#ADMINISTRADOR

@login_required
@role_required('Administrador')
def AdministradorLista(request):
    if not request.user.is_authenticated or request.user.rol.nombre != 'Administrador':
        raise PermissionDenied
    rol_administrador = Rol.objects.get(nombre='Administrador')
    administradores = Usuario.objects.filter(rol=rol_administrador)
    return render(request, 'administrador/administrador_lista.html', {'object_list': administradores})


@login_required
@role_required('Administrador')
def AdministradorRegistro(request):
    if request.method == 'POST':
        administrador_form = AdministradorForm(request.POST)
        persona_form = PersonaForm(request.POST)
        if administrador_form.is_valid() and persona_form.is_valid():
            persona = persona_form.save()
            administrador = administrador_form.save(commit=False)
            administrador.persona = persona
            administrador.rol = Rol.objects.get(nombre='administrador')
            administrador.save()
            messages.success(request, 'Administrador registrado exitosamente.',extra_tags='administrador')
            return redirect('administrador_lista')
    else:
        administrador_form = AdministradorForm()
        persona_form = PersonaForm()
    return render(request, 'administrador/nuevo_administrador.html', {'administrador_form': administrador_form, 'persona_form': persona_form})

@login_required
@role_required('Administrador')
def AdministradorActualizar(request, administrador_id):
    try:

        administrador = get_object_or_404(Usuario, id=administrador_id, rol__nombre='Administrador')
    
        if request.method == 'POST':
            administrador_form = AdministradorUpdateForm(request.POST, instance=administrador)
            persona_form = PersonaUpdateForm(request.POST, instance=administrador.persona)
            password_change_form = CustomPasswordChangeForm(user=administrador, data=request.POST)
        
            if administrador_form.is_valid() and persona_form.is_valid() and password_change_form.is_valid():
                administrador_form.save()
                persona_form.save()
                password_change_form.save()
                messages.success(request, 'Administrador actualizado exitosamente.',extra_tags='administrador')
                return redirect('administrador_lista')
        else:
            administrador_form = AdministradorUpdateForm(instance=administrador)
            persona_form = PersonaUpdateForm(instance=administrador.persona)
            password_change_form = CustomPasswordChangeForm(user=administrador)
        return render(request, 'administrador/administrador_actualizar.html', {
            'administrador_form': administrador_form,
            'persona_form': persona_form,
            'password_change_form': password_change_form
        })
    except Http404:
        return render(request, 'errors/404.html', status=404)

@login_required
@role_required('Administrador')
def AdministradorEliminar(request, administrador_id):
    administrador = get_object_or_404(Usuario, id=administrador_id, rol__nombre='administrador')
    if request.method == 'POST':
        administrador.delete()
        messages.success(request, 'Administrador eliminado exitosamente.',extra_tags='administrador')
        return redirect('administrador_lista')
    return render(request, 'administrador/administrador_eliminar.html', {'administrador': administrador})

#TIPO ROL
@login_required
@role_required('Administrador')
def TipoRolLista(request):
    tipo_roles = Rol.objects.all()
    return render(request, 'tiporol/tiporol_lista.html', {'object_list': tipo_roles})

@login_required
@role_required('Administrador')
def RolRegistro(request):
    if request.method == 'POST':
        rol_form = TipoRolForm(request.POST)
        if rol_form.is_valid():
            rol_form.save()
            messages.success(request, 'Rol registrado exitosamente.',extra_tags='rol')
            return redirect('rol_lista')
    else:
        rol_form = TipoRolForm()

    return render(request, 'tiporol/nuevo_tiporol.html', {'rol_form': rol_form})

@login_required
@role_required('Administrador')
def TipoRolActualizar(request, rol_id):
    try:
        rol = get_object_or_404(Rol, id=rol_id)
        if request.method == 'POST':
           rol_form = TipoRolForm(request.POST, instance=rol)
           if rol_form.is_valid():
               rol_form.save()
               messages.success(request, 'Rol actualizado exitosamente.',extra_tags='rol')
               return redirect('rol_lista')
        else:
            rol_form = TipoRolForm(instance=rol)
        return render(request, 'tiporol/actualizar_tiporol.html', {'rol_form': rol_form})
    except Http404:
        return render(request, 'errors/404.html', status=404)
    
@login_required
@role_required('Administrador')
def TipoRolEliminar(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado exitosamente.',extra_tags='rol')
        return redirect('rol_lista')
    return render(request, 'tiporol/tiporol_eliminar.html', {'rol': rol})

#TIPO DOCUMENTO

@login_required
@role_required('Administrador')
def TipoDocumentolLista(request):
    tipo_documentos = TipoIdentificacion.objects.all()
    return render(request, 'tipodocumento/tipodocumento_lista.html', {'object_list': tipo_documentos})


@login_required
@role_required('Administrador')
def TipoDocumentoRegistro(request):
    if request.method == 'POST':
        documento_form = TipoIdentificacionForm(request.POST)
        if documento_form.is_valid():
            documento_form.save()
            messages.success(request, 'Documento registrado exitosamente.',extra_tags='documento')
            return redirect('documento_lista')
    else:
        documento_form = TipoIdentificacionForm()

    return render(request, 'tipodocumento/nuevo_tipodocumento.html', {'documento_form': documento_form})


@login_required
@role_required('Administrador')
def TipoDocumentoActualizar(request, documento_id):
    documento = get_object_or_404(TipoIdentificacion, id=documento_id)
    if request.method == 'POST':
        documento_form = TipoIdentificacionForm(request.POST, instance=documento)
        if documento_form.is_valid():
            documento_form.save()
            messages.success(request, 'Documento actualizado exitosamente.',extra_tags='documento')
            return redirect('documento_lista')
    else:
        documento_form = TipoIdentificacionForm(instance=documento)

    return render(request, 'tipodocumento/actualizar_tipodocumento.html', {'documento_form': documento_form})


@login_required
@role_required('Administrador')
def TipoDocumentoEliminar(request, documento_id):
    documento = get_object_or_404(TipoIdentificacion, id=documento_id)
    if request.method == 'POST':
        documento.delete()
        messages.success(request, 'Documento eliminado exitosamente.',extra_tags='documento')
        return redirect('documento_lista')
    return render(request, 'tipodocumento/tipodocumento_eliminar.html', {'documento': documento})



# ESTADO SOLICITUD
@login_required
@role_required('Administrador')
def EstadoSolicitudLista(request):
    estados = EstadoSolicitud.objects.all()
    return render(request, 'estadosolicitud/estado_solicitud_lista.html', {'object_list': estados})

@login_required
@role_required('Administrador')
def EstadoSolicitudRegistro(request):
    if request.method == 'POST':
        estado_form = EstadoSolicitudForm(request.POST)
        if estado_form.is_valid():
            estado_form.save()
            messages.success(request, 'Estado de solicitud registrado exitosamente.', extra_tags='estado')
            return redirect('estado_solicitud_lista')
    else:
        estado_form = EstadoSolicitudForm()
    return render(request, 'estadosolicitud/nuevo_estado_solicitud.html', {'estado_form': estado_form})

@login_required
@role_required('Administrador')
def EstadoSolicitudActualizar(request, estado_id):
    estado = get_object_or_404(EstadoSolicitud, id=estado_id)
    if request.method == 'POST':
        estado_form = EstadoSolicitudForm(request.POST, instance=estado)
        if estado_form.is_valid():
            estado_form.save()
            messages.success(request, 'Estado de solicitud actualizado exitosamente.', extra_tags='estado')
            return redirect('estado_solicitud_lista')
    else:
        estado_form = EstadoSolicitudForm(instance=estado)
    return render(request, 'estadosolicitud/actualizar_estado_solicitud.html', {'estado_form': estado_form})

@login_required
@role_required('Administrador')
def EstadoSolicitudEliminar(request, estado_id):
    estado = get_object_or_404(EstadoSolicitud, id=estado_id)
    if request.method == 'POST':
        estado.delete()
        messages.success(request, 'Estado de solicitud eliminado exitosamente.', extra_tags='estado')
        return redirect('estado_solicitud_lista')
    return render(request, 'estadosolicitud/estado_solicitud_eliminar.html', {'estado': estado})



# SOLICITUD MESA PARTE
@login_required
@role_required('Usuario')
def SolicitudMesaPartListaUsuario(request):
    solicitudes = SolicitudMesaParte.objects.filter(usuario=request.user)
    return render(request, 'solicitudmesaparte/mesadeparte_lista.html', {'object_list': solicitudes})

@login_required
@role_required('Administrador')
def SolicitudMesaPartListaGeneral(request):
    solicitudes = SolicitudMesaParte.objects.all()
    return render(request, 'solicitudmesaparte/mesadeparte_lista admin.html', {'object_list': solicitudes})


@login_required
@role_required('Usuario')
def SolicitudMesaParteRegistro(request):
    if request.method == 'POST':
        solicitud_form = SolicitudMesaParteForm(request.POST, request.FILES) 
        
        if solicitud_form.is_valid():
            solicitud = solicitud_form.save(commit=False)
            campos_casillas = [solicitud_form.cleaned_data[f'casilla{i}'] for i in range(1, 9)]
            solicitud.fundamento_solicitud = ', '.join(filter(None, campos_casillas))
            solicitud.usuario = request.user
            solicitud.estado = EstadoSolicitud.objects.get(nombre='Enviado')
            solicitud.fecha_solicitud = timezone.now().date()
            solicitud.save()
            messages.success(request, 'Administrador registrado exitosamente.',extra_tags='solicitud')
            return redirect('solicitud_mesa_parte_lista_usuario') 
    else:
        solicitud_form = SolicitudMesaParteForm()
    return render(request, 'solicitudmesaparte/nuevo_solicitudmesaparte.html', {'solicitud_form': solicitud_form})

@login_required
@role_required('Usuario')
def SolicitudMesaParteActualizarUsuario(request, solicitud_id):
    try:
        solicitud = get_object_or_404(SolicitudMesaParte, id=solicitud_id, usuario=request.user)
        if solicitud.usuario != request.user:
            return error_403(request)
        if request.method == 'POST':
           solicitud_form = SolicitudMesaParteForm(request.POST, request.FILES, instance=solicitud)
           if solicitud_form.is_valid():
               solicitud = solicitud_form.save(commit=False)
               campos_casillas = [solicitud_form.cleaned_data.get(f'casilla{i}', '') for i in range(1, 9)]
               solicitud.fundamento_solicitud = ', '.join(filter(None, campos_casillas))
               solicitud.fecha_solicitud = SolicitudMesaParte.objects.filter(id=solicitud_id).values_list('fecha_solicitud', flat=True).first()
               solicitud.save()
               messages.success(request, 'Solicitud actualizada exitosamente.', extra_tags='solicitud')
               return redirect('solicitud_mesa_parte_lista_usuario')
        else:
            solicitud_form = SolicitudMesaParteForm(instance=solicitud)
        return render(request, 'solicitudmesaparte/actualizar_solicictudmesaparte.html', {'solicitud_form': solicitud_form})
    except Http404:
        return render(request, 'errors/404.html', status=404)
    
@login_required
@role_required('Administrador')
def SolicitudMesaParteActualizarGeneral(request, solicitud_id):
    try:
        solicitud = get_object_or_404(SolicitudMesaParte, id=solicitud_id)
        if request.method == 'POST':
            solicitud_form = SolicitudMesaParteFormAdministrador(request.POST, request.FILES, instance=solicitud)
            if solicitud_form.is_valid():
                solicitud_form.save()
                messages.success(request, 'Solicitud actualizada exitosamente.', extra_tags='solicitudAd')
                return redirect('solicitud_mesa_parte_lista')
            else:
                messages.error(request, 'Error al actualizar la solicitud. Revise los campos del formulario.')
        else:
            solicitud_form = SolicitudMesaParteFormAdministrador(instance=solicitud)
        return render(request, 'solicitudmesaparte/actualizar_admin_solicitudmesaparte.html', {'solicitud_form': solicitud_form, 'solicitud': solicitud})
    except Http404:
        return render(request, 'errors/404.html', status=404)
    
    except PermissionDenied:
        return render(request, 'errors/403.html', status=403)
    
@login_required

def descargar_archivo_adjunto(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMesaParte, id=solicitud_id)
    if solicitud.archivo_adjunto:
        file_path = solicitud.archivo_adjunto.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404("Archivo no encontrado")
    else:
        raise Http404("Archivo no adjunto a la solicitud")

@login_required
@role_required('Usuario')
def SolicitudMesaParteEliminar(request, solicitud_id):
    try:
        solicitud = get_object_or_404(SolicitudMesaParte, id=solicitud_id, usuario=request.user)
        fecha_limite = solicitud.fecha_solicitud + timedelta(days=5)
        if timezone.now().date() > fecha_limite:
           messages.error(request, 'No se puede eliminar la solicitud después de 5 días de su creación.', extra_tags='solicitud')
           return redirect('solicitud_mesa_parte_lista_usuario')
        if solicitud.estado.nombre == 'Aceptado':
            messages.error(request, 'No se puede eliminar el solicitud cuando su estado es "Aceptado".', extra_tags='solicitud')
            return redirect('solicitud_mesa_parte_lista_usuario')
        if solicitud.estado.nombre == 'Rechazado':
            messages.error(request, 'No se puede eliminar el solicitud cuando su estado es "Rechazado".', extra_tags='solicitud')
            return redirect('solicitud_mesa_parte_lista_usuario')
        if solicitud.estado.nombre == 'Falta informacion':
            messages.error(request, 'No se puede eliminar el solicitud cuando su estado es "Falta informacion".', extra_tags='solicitud')
            return redirect('solicitud_mesa_parte_lista_usuario')

        if request.method == 'POST':
           solicitud.delete()
           messages.success(request, 'Solicitud eliminada exitosamente.')
           return redirect('solicitud_mesa_parte_lista_usuario')
        return render(request, 'solicitudmesaparte/eliminar_solicitudmesaparte.html', {'solicitud': solicitud})
    except Http404:
        return render(request, 'errors/404.html', status=404)



@login_required
@role_required('Usuario')
def ReporteIncidenciaListaUsuario(request):
    reportes = ReporteIncidente.objects.filter(usuario=request.user)
    return render(request, 'reporteincidente/reporte_lista.html', {'object_list': reportes})

@login_required
@role_required('Administrador')
def ReporteIncidenciaListaGeneral(request):
    reportes = ReporteIncidente.objects.all()
    return render(request, 'reporteincidente/reporte_lista_general.html', {'object_list': reportes})



@login_required
@role_required('Usuario')
def ReporteIncidenteRegistro(request):
    if request.method == 'POST':
        incidente_form = ReporteIncidenteForm(request.POST, request.FILES)
        
        if incidente_form.is_valid():
            incidente = incidente_form.save(commit=False)
            incidente.usuario = request.user
            incidente.estado = EstadoReporte.objects.get(nombre='Enviado')
            incidente.fecha = timezone.now().date()
            incidente.hora = timezone.now().time()
            incidente.save()
            messages.success(request, 'Reporte de incidente registrado exitosamente.', extra_tags='reporte')
            return redirect('lista_reportes_incidente') 
    else:
        incidente_form = ReporteIncidenteForm()
    return render(request, 'reporteincidente/nuevo_reporte.html', {'incidente_form': incidente_form})

@login_required
@role_required('Usuario')
def ReporteIncidenteActualizarUsuario(request, incidente_id):
    try:
        incidente = get_object_or_404(ReporteIncidente, id=incidente_id, usuario=request.user)
        if request.method == 'POST':
            incidente_form = ReporteIncidenteForm(request.POST, request.FILES, instance=incidente)
            if incidente_form.is_valid():
                incidente = incidente_form.save(commit=False)
                incidente.fecha = ReporteIncidente.objects.filter(id=incidente_id).values_list('fecha', flat=True).first()
                incidente.hora = ReporteIncidente.objects.filter(id=incidente_id).values_list('hora', flat=True).first()
                incidente.save()
                messages.success(request, 'Reporte de incidente actualizado exitosamente.', extra_tags='reporte')
                return redirect('lista_reportes_incidente')
        else:
            incidente_form = ReporteIncidenteForm(instance=incidente)
        return render(request, 'reporteincidente/actualizar_reporte.html', {'incidente_form': incidente_form})
    except Http404:
        return render(request, 'errors/404.html', status=404)

@login_required
@role_required('Administrador')
def ReporteIncidenteActualizarGeneral(request, incidente_id):
    try:
        incidente = get_object_or_404(ReporteIncidente, id=incidente_id)
        if request.method == 'POST':
            incidente_form = ReporteIncidenteFormAdministrador(request.POST, request.FILES, instance=incidente)
            if incidente_form.is_valid():
                incidente = incidente_form.save(commit=False)
                incidente.fecha = ReporteIncidente.objects.filter(id=incidente_id).values_list('fecha', flat=True).first()
                incidente.hora = ReporteIncidente.objects.filter(id=incidente_id).values_list('hora', flat=True).first()
                incidente.save()
                messages.success(request, 'Reporte de incidente actualizado exitosamente.', extra_tags='reportess')
                return redirect('lista_reportes_incidente_general')
            else:
                messages.error(request, 'Error al actualizar el reporte. Revise los campos del formulario.')
        else:
            incidente_form = ReporteIncidenteFormAdministrador(instance=incidente)
        return render(request, 'reporteincidente/actualizar_reporte_admin.html', {'incidente_form': incidente_form, 'incidente': incidente})
    except Http404:
        return render(request, 'errors/404.html', status=404)
    except PermissionDenied:
        return render(request, 'errors/403.html', status=403)

def descargar_capturas(request, incidente_id):
    incidente = get_object_or_404(ReporteIncidente, id=incidente_id)
    if incidente.imagen:
        file_path = incidente.imagen.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404("Imagen no encontrado")
    else:
        raise Http404("imagen no adjunto en Reportes")

@login_required
@role_required('Usuario')
def ReporteIncidenteEliminar(request, incidente_id):
    try:
        incidente = get_object_or_404(ReporteIncidente, id=incidente_id, usuario=request.user)
        fecha_limite = incidente.fecha + timedelta(days=5)
        if timezone.now().date() > fecha_limite:
            messages.error(request, 'No se puede eliminar el reporte después de 5 días de su creación.', extra_tags='reporte')
            return redirect('lista_reportes_incidente')

        if incidente.estado.nombre == 'Resuelto':
            messages.error(request, 'No se puede eliminar el reporte cuando su estado es "Resuelto".', extra_tags='reporte')
            return redirect('lista_reportes_incidente')

        if request.method == 'POST':
            incidente.delete()
            messages.success(request, 'Reporte de incidente eliminado exitosamente.')
            return redirect('lista_reportes_incidente')
        return render(request, 'reporteincidente/eliminar_reporte.html', {'incidente': incidente})
    except Http404:
        return render(request, 'errors/404.html', status=404)


#Cerrar Seccion
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Has sido desconectado',extra_tags='logout')
    return redirect('login')
