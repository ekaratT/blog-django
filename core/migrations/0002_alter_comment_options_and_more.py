# Generated by Django 5.0.3 on 2024-03-31 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='core_commen_created_c3602f_idx'),
        ),
    ]
