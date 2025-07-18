# Generated by Django 5.2.3 on 2025-07-04 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Facilityadmin', '0002_initial'),
        ('HealthcareW', '0001_initial'),
        ('Sysadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Guardian', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='child',
            name='national_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='HealthcareW.guardian'),
        ),
        migrations.AddField(
            model_name='notification',
            name='guardian',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='HealthcareW.guardian'),
        ),
        migrations.AddField(
            model_name='vaccinationrecord',
            name='administered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Facilityadmin.healthcarew'),
        ),
        migrations.AddField(
            model_name='vaccinationrecord',
            name='child_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccination_records', to='HealthcareW.child'),
        ),
        migrations.AddField(
            model_name='vaccinationrecord',
            name='v_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sysadmin.vaccine'),
        ),
        migrations.AlterUniqueTogether(
            name='growthcurve',
            unique_together={('child_id', 'curve_type', 'date_calculated')},
        ),
        migrations.AlterUniqueTogether(
            name='growthrecord',
            unique_together={('child_id', 'date_recorded')},
        ),
        migrations.AlterUniqueTogether(
            name='vaccinationrecord',
            unique_together={('child_id', 'v_ID', 'doseNumber')},
        ),
    ]
