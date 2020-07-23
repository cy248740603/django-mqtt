# Generated by Django 3.0.8 on 2020-07-20 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='分类')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceID', models.CharField(max_length=16, verbose_name='设备ID')),
                ('info', models.CharField(max_length=200, verbose_name='基本信息')),
                ('created_time', models.DateTimeField(verbose_name='生成时间')),
            ],
            options={
                'verbose_name': '设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标签')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='功率')),
                ('created_time', models.DateTimeField(verbose_name='生成时间')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='server.Device', verbose_name='设备')),
            ],
            options={
                'verbose_name': '数据',
                'verbose_name_plural': '数据',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='标题')),
                ('intro', models.TextField(blank=True, max_length=200, verbose_name='摘要')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('tags', models.ManyToManyField(blank=True, to='server.Tags')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
    ]