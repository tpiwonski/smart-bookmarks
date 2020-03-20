# Generated by Django 2.2.10 on 2020-03-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_title_description_source_to_page_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='page',
            name='source',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]