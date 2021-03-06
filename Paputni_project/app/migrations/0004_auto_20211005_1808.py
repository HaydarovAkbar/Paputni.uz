# Generated by Django 3.2.7 on 2021-10-05 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_passenger_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.order'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='user_status',
            field=models.CharField(choices=[('Tasdiqlangan', 'Tasdiqlangan'), ('Tasdiqlanmagan', 'Tasdiqlanmagan')], default='Tasdiqlangan', max_length=40),
        ),
    ]
