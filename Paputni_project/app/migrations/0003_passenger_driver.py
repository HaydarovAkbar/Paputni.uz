# Generated by Django 3.2.7 on 2021-10-05 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='driver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.order'),
        ),
    ]
