# Generated by Django 2.2.10 on 2020-03-18 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_require_title_description_source_in_page_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexBookmark',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bookmark', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='_index_bookmark', to='core.Bookmark')),
            ],
            options={
                'db_table': 'index_bookmark',
            },
        ),
        migrations.AddConstraint(
            model_name='indexbookmark',
            constraint=models.UniqueConstraint(fields=('bookmark',), name='uq_bookmark_id'),
        ),
    ]
