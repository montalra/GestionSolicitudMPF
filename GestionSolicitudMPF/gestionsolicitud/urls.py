
from django.urls import path,re_path


from .views import UsuarioRegistro, UsuarioLista,UsuarioActualizar,UsuarioEliminar
from .views import AdministradorRegistro,AdministradorLista,AdministradorActualizar,AdministradorEliminar
from .views import RolRegistro, TipoRolLista,TipoRolActualizar,TipoRolEliminar
from .views import TipoDocumentoRegistro,TipoDocumentolLista,TipoDocumentoActualizar,TipoDocumentoEliminar
from .views import EstadoSolicitudLista,EstadoSolicitudRegistro,EstadoSolicitudActualizar,EstadoSolicitudEliminar
from .views import SolicitudMesaPartListaUsuario,SolicitudMesaPartListaGeneral,SolicitudMesaParteRegistro,SolicitudMesaParteActualizarUsuario,SolicitudMesaParteActualizarGeneral,SolicitudMesaParteEliminar,descargar_archivo_adjunto
from .views import ReporteIncidenteRegistro,ReporteIncidenciaListaUsuario,ReporteIncidenciaListaGeneral,ReporteIncidenteActualizarUsuario,ReporteIncidenteEliminar,ReporteIncidenteActualizarGeneral,descargar_capturas
from .views import logout_user

from .import views


urlpatterns = [
    path('', views.login_user, name='login'),
   
    path('menu/principal/', views.menuPrincipal, name='menu_principal'),
    path('panel/gestion/', views.menuControl, name='panel_control'),
    path ('terminos-y-condiciones/',views.Terminosycondiciones, name='terminos_condiciones'),
    path('errors/403', views.error_403, name='error_403'),

    path('myaccount/registrar?/', UsuarioRegistro, name='nuevo_usuario'),
    path('usuario/listar/', UsuarioLista, name='usuario_lista'),
    path('usuarios/actualizar/<int:usuario_id>/', UsuarioActualizar, name='actualizar_usuario'),
    path('ususario/eliminar/<int:usuario_id>/', UsuarioEliminar, name='usuario_eliminar'),

    path('administrador/nuevo/', AdministradorRegistro, name='nuevo_administrador'),
    path('administrador/listar/', AdministradorLista, name='administrador_lista'),
    path('administrador/actualizar/<int:administrador_id>/', AdministradorActualizar, name='administrador_actualizar'),
    path('administrador/<int:administrador_id>/eliminar', AdministradorEliminar, name='administrador_eliminar'),

    path('tipo-rol/nuevo/', RolRegistro, name='nuevo_rol'),
    path('tipo-rol/listar/', TipoRolLista, name='rol_lista'),
    path('tipo-rol/actualizar/<int:rol_id>/', TipoRolActualizar, name='rol_actualizar'),
    path('tipo-rol/<int:rol_id>/eliminar', TipoRolEliminar, name='rol_eliminar'),

    path('tipo-documento/nuevo/', TipoDocumentoRegistro, name='nuevo_documento'),
    path('tipo-documento/listar/', TipoDocumentolLista, name='documento_lista'),
    path('tipo-documento/actualizar/<int:documento_id>/', TipoDocumentoActualizar, name='documento_actualizar'),
    path('tipo-documento/<int:documento_id>/eliminar', TipoDocumentoEliminar, name='documento_eliminar'),


    # Estado Solicitud
    path('estados/', EstadoSolicitudLista, name='estado_solicitud_lista'),
    path('estados/nuevo/', EstadoSolicitudRegistro, name='estado_solicitud_registro'),
    path('estados/actualizar/<int:estado_id>/', EstadoSolicitudActualizar, name='estado_solicitud_actualizar'),
    path('estados/eliminar/<int:estado_id>/', EstadoSolicitudEliminar, name='estado_solicitud_eliminar'),

    # Solicitud Mesa Parte
    path('solicitudes/', SolicitudMesaPartListaGeneral, name='solicitud_mesa_parte_lista'),
    path('mis-solicitudes/', SolicitudMesaPartListaUsuario, name='solicitud_mesa_parte_lista_usuario'),
    path('solicitudes/nueva/', SolicitudMesaParteRegistro, name='nuevo_solicitud_mesaparte'),
    path('solicitudes/actualizar/<int:solicitud_id>/', SolicitudMesaParteActualizarGeneral, name='solicitud_mesa_parte_actualizar_admin'),
    path('solicitudes/descargar/<int:solicitud_id>/', descargar_archivo_adjunto, name='descargar_archivo_adjunto'),

    path('mis-solicitudes/actualizar/<int:solicitud_id>/', SolicitudMesaParteActualizarUsuario, name='solicitud_mesa_parte_actualizar_usuario'),
    path('solicitudes/eliminar/<int:solicitud_id>/', SolicitudMesaParteEliminar, name='solicitud_mesa_parte_eliminar'),


    path('reporte/nueva/', ReporteIncidenteRegistro, name='nuevo_reporte_incidente'),
    path('mis_reportes/', ReporteIncidenciaListaUsuario, name='lista_reportes_incidente'),
    path('reportes/', ReporteIncidenciaListaGeneral, name='lista_reportes_incidente_general'),
    path('mis-reporte/actualizar/<int:incidente_id>/', ReporteIncidenteActualizarUsuario, name='reporte_incidente_actualizar_usuario'),
    path('reportes/actualizar/<int:incidente_id>/', ReporteIncidenteActualizarGeneral, name='reporte_incidente_actualizar_admin'),
    path('reportes/descargar/<int:incidente_id>/', descargar_capturas, name='descargar_capturas'),
    path('reportes/eliminar/<int:incidente_id>/', ReporteIncidenteEliminar, name='reporte_incidente_eliminar'),

    path('logout/', logout_user, name='logout'),

    re_path(r'^.*$', views.error_404, name='error_404')

]
