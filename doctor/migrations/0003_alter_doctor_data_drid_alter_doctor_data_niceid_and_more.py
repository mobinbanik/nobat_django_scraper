# Generated by Django 5.0.7 on 2024-08-18 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_image_office_id_alter_city_number_alter_image_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='data_drid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='data_niceid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='like_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
