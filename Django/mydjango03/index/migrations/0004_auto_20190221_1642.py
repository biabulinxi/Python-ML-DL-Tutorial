# Generated by Django 2.1.4 on 2019-02-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_author_isactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='age',
            field=models.IntegerField(verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='author',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='激活'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(db_index=True, max_length=30, unique=True, verbose_name='姓名'),
        ),
        migrations.AlterModelTable(
            name='author',
            table='author',
        ),
    ]
