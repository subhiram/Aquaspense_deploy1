# Generated by Django 4.1.5 on 2023-05-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_feed_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_user',
            fields=[
                ('temp_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('user_type', models.BooleanField(default=False)),
                ('otp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user_detail',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('user_type', models.BooleanField(default=False)),
            ],
        ),
    ]
