# Generated by Django 5.1.1 on 2024-10-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'ordering': ['product'], 'verbose_name': 'عکس', 'verbose_name_plural': 'عکس ها'},
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
