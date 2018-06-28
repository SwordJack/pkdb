# Generated by Django 2.0.6 on 2018-06-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0002_publication_authors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=30, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Else'), (2, 'Dynamic Single'), (3, 'Dynamic Multiple'), (4, 'Static Single'), (5, 'Static Multiple')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='publication',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='study',
            name='publication',
        ),
        migrations.RemoveField(
            model_name='study',
            name='type',
        ),
        migrations.AddField(
            model_name='study',
            name='authors',
            field=models.ManyToManyField(blank=True, to='studies.Author'),
        ),
        migrations.AddField(
            model_name='study',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='study'),
        ),
        migrations.AddField(
            model_name='study',
            name='pmid',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study',
            name='title',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Publication',
        ),
        migrations.AddField(
            model_name='intervention',
            name='study',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, to='studies.Study'),
        ),
    ]
