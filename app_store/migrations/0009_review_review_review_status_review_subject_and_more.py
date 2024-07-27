# Generated by Django 4.0.3 on 2024-07-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0008_review_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='review',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(),
        ),
    ]
