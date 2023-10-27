from django.db import models


class Municipio(models.Model):
    """
    Modelo de Municipios
    """

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"


class Rendicion(models.Model):
    """
    Modelo de Rendiciones Municipales
    """

    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    anio = models.IntegerField()
    periodo = models.IntegerField()
    fecha_vto_presentacion = models.DateField()

    class Meta:
        verbose_name = "Rendicion"
        verbose_name_plural = "Rendiciones"


class Presentacion(models.Model):
    """
    Modelo de Presentaciones de Rendiciones Municipales
    """

    rendicion = models.ForeignKey(Rendicion, on_delete=models.PROTECT)
    fecha_presentacion = models.DateField(blank=True, null=True)
    numero_presentacion = models.IntegerField()
    estado = models.BooleanField()

    class Meta:
        verbose_name = "Presentacion"
        verbose_name_plural = "Presentaciones"


class DocumentoRequerido(models.Model):
    """
    Modelo de Documentos Requeridos
    """

    descripcion = models.CharField(max_length=200)
    fecha_vig_desde = models.DateField()
    fecha_vig_hasta = models.DateField()
    obligatorio = models.BooleanField()
    multicarga = models.BooleanField()
    extensiones_permitidas = models.CharField(
        max_length=200, help_text="Separar con coma (,) cada extensión"
    )

    def get_extensiones_permitidas(self):
        return self.extensiones_permitidas.split(",")

    class Meta:
        verbose_name = "Documento Requerido"
        verbose_name_plural = "Documentos Requeridos"


class DocumentoRendicion(models.Model):
    """
    Modelo de Documentos de Rendiciones Municipales
    """

    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    documento_requerido = models.ForeignKey(
        DocumentoRequerido, on_delete=models.PROTECT
    )
    archivo = models.FileField(upload_to="documentos_rendiciones/")

    class Meta:
        verbose_name = "Documento de Rendicion"
        verbose_name_plural = "Documentos de Rendiciones"
