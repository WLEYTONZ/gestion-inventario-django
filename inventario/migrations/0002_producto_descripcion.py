from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("inventario", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="descripcion",
            field=models.TextField(default="", verbose_name="Descripción"),
            preserve_default=False,
        ),
    ]
