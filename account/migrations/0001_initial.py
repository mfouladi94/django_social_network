# Generated by Django 4.2.1 on 2023-05-24 16:46

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50, unique=True, verbose_name='user name')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='name')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='avatar')),
                ('friends_count', models.IntegerField(default=0, verbose_name='Number of friends')),
                ('posts_count', models.IntegerField(default=0, verbose_name='Number of posts')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is super user')),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='time of joining')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login ')),
                ('friends', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='friends')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]