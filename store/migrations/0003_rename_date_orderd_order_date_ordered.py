# Generated by Django 5.1.1 on 2024-11-18 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_productimage_image_alter_productimage_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_orderd',
            new_name='date_ordered',
        ),
    ]
