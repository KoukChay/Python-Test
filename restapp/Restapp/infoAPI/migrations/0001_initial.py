# Generated by Django 4.2.5 on 2023-10-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Zaw Hein', max_length=30)),
                ('email', models.CharField(default='example@gmail.com', max_length=50)),
                ('phno', models.IntegerField(default=9260000000, max_length=10)),
                ('degree', models.CharField(default='BE-Electronics', max_length=50)),
            ],
        ),
    ]