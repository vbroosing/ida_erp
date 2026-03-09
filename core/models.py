from django.db import models

# Para referenciar al usuario
# from django.conf import settings 

# MODELO BASE ABSTRACTO: es para no repetir valores de trazabilidad.
class AuditModel(models.Model):
    """
    Modelo base que incluye campos de auditoría y estado.
    No crea una tabla en la BD, solo sirve para heredar.
    """
    is_active = models.BooleanField(default=True, verbose_name="Es activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")
    
    # Opcional(futuro): Si ya está configurado Auth, descomentar esto
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.SET_NULL, 
    #     null=True, blank=True, 
    #     related_name="%(class)s_created",
    #     verbose_name="Creado por"
    # )
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.SET_NULL, 
    #     null=True, blank=True, 
    #     related_name="%(class)s_updated",
    #     verbose_name="Actualizado por"
    # )

    class Meta:
        abstract = True
