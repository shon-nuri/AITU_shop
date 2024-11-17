# Generated by Django 5.1.1 on 2024-11-17 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_image_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('hoodie', 'Hoodies'), ('tshirt', 'T-Shirts'), ('sale', 'Sale')], max_length=50, null=True),
        ),
    ]
