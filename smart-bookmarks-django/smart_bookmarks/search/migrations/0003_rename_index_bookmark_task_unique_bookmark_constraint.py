# Generated by Django 2.2.10 on 2020-03-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0002_replace_index_bookmark_with_index_bookmark_task"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="indexbookmarktask", name="uq_bookmark_id",
        ),
        migrations.AddConstraint(
            model_name="indexbookmarktask",
            constraint=models.UniqueConstraint(
                fields=("bookmark",), name="uq_index_bookmark_task_bookmark_id"
            ),
        ),
    ]
