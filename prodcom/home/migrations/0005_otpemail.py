# Generated by Django 3.2.7 on 2021-11-09 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_delete_otpemail'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPemail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255)),
                ('passw', models.CharField(max_length=50)),
                ('numcode', models.CharField(max_length=10)),
                ('time_stp', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp', models.IntegerField()),
            ],
        ),
    ]
