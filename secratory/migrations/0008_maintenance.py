# Generated by Django 4.0 on 2022-03-01 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secratory', '0007_alter_gallery_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('pay_time', models.DateTimeField(auto_now_add=True)),
                ('month', models.CharField(max_length=15)),
                ('year', models.IntegerField()),
                ('pay_id', models.CharField(max_length=20, unique=True)),
                ('pay_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secratory.adminsec')),
            ],
        ),
    ]