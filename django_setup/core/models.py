from django.core.exceptions import ValidationError
from django.db import models


class Municipio(models.Model):
    """
    Modelo de Municipios
    En este prototipo, los municipios solo se crean/editan desde el panel de administración
    """

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"


class Rendicion(models.Model):
    """
    Modelo de Rendiciones Municipales
    En este prototipo, las rendiciones solo se crean/editan desde el panel de administración
    """

    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    anio = models.IntegerField()
    periodo = models.IntegerField()
    fecha_vto_presentacion = models.DateField()

    def get_estado(self):
        if self.presentacion_set.count() == 0:
            return "No Presentada"
        else:
            # Obtener el estado de la ultima presentacion
            return self.presentacion_set.last().get_estado()

    def get_nro_presentacion(self):
        if self.presentacion_set.count() == 0:
            return 0
        else:
            return self.presentacion_set.last().nro_presentacion

    def __str__(self):
        return f"{self.municipio.nombre} - {self.anio} - {self.periodo}"

    class Meta:
        verbose_name = "Rendición"
        verbose_name_plural = "Rendiciones"


class Presentacion(models.Model):
    """
    Modelo de Presentaciones de Rendiciones Municipales
    """

    rendicion = models.ForeignKey(Rendicion, on_delete=models.PROTECT)
    nro_presentacion = models.IntegerField()
    fecha_presentacion = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=False)

    def get_estado(self):
        if self.estado:
            return "Presentada"
        else:
            return "En Carga"

    def __str__(self):
        return f"{self.rendicion} - {self.nro_presentacion}"

    class Meta:
        verbose_name = "Presentación"
        verbose_name_plural = "Presentaciones"


class DocumentoRequerido(models.Model):
    """
    Modelo de Documentos Requeridos
    En este prototipo, los documentos requeridos solo se crean/editan desde el panel de administración
    Los documentos requeridos son todos los documentos que se deben presentar en una rendición
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

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Documento Requerido"
        verbose_name_plural = "Documentos Requeridos"


class Documento(models.Model):
    """
    Modelo de Documentos para las Presentaciones de Rendiciones Municipales
    """

    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    documento_requerido = models.ForeignKey(
        DocumentoRequerido, on_delete=models.PROTECT
    )

    def file_directory_path(self, filename):
        return 'doc/presentacion-{0}/{1}'.format(self.presentacion.pk, filename)

    archivo = models.FileField(upload_to=file_directory_path)

    def nombre_archivo(self):
        return self.archivo.name.split("/")[-1]

    def clean(self):
        # Validar que la extension del archivo sea una de las permitidas
        extension = self.archivo.name.split(".")[-1]
        if extension not in self.documento_requerido.get_extensiones_permitidas():
            raise ValidationError(
                f"La extensión del archivo es incorrecta. Las extensiones permitidas son: "
                f"{self.documento_requerido.get_extensiones_permitidas()}"
            )

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
