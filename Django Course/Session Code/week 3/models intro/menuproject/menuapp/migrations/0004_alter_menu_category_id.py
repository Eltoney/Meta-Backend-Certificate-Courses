# Generated by Django 4.1.3 on 2022-12-04 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0003_menucategory_rename_name_menu_menu_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='category_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='menuapp.menucategory'),
        ),
    ]
