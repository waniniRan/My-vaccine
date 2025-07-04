# Generated by Django 5.2.3 on 2025-07-04 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Facilityadmin', '0001_initial'),
        ('Sysadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcarew',
            name='Facility_admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_workers', to='Sysadmin.facilityadmin'),
        ),
        migrations.AddField(
            model_name='healthcarew',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='Sysadmin.healthfacility'),
        ),
        migrations.AddField(
            model_name='healthcarew',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Worker', to=settings.AUTH_USER_MODEL),
        ),
    ]
