# Generated by Django 4.2.21 on 2025-07-16 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treeapp', '0003_remove_marriage_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marriage',
            name='family',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='marriages', to='treeapp.family'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='husband',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='marriages_as_husband', to='treeapp.person'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='wife',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='marriages_as_wife', to='treeapp.person'),
        ),
    ]
