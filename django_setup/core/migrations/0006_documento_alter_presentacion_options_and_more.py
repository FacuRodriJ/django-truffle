# Generated by Django 4.2.6 on 2023-11-06 12:22

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_numero_presentacion_presentacion_nro_presentacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to=core.models.Documento.file_directory_path)),
                ('documento_requerido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.documentorequerido')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.AlterModelOptions(
            name='presentacion',
            options={'verbose_name': 'Presentación', 'verbose_name_plural': 'Presentaciones'},
        ),
        migrations.AlterModelOptions(
            name='rendicion',
            options={'verbose_name': 'Rendición', 'verbose_name_plural': 'Rendiciones'},
        ),
        migrations.DeleteModel(
            name='DocumentoRendicion',
        ),
        migrations.AddField(
            model_name='documento',
            name='presentacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.presentacion'),
        ),
    ]
