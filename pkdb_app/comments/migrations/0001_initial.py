# Generated by Django 2.0.6 on 2018-08-14 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interventions', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_created=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('characteristica', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='subjects.Characteristica')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='subjects.Group')),
                ('groupset', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='subjects.GroupSet')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='subjects.Individual')),
                ('individualset', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='subjects.IndividualSet')),
                ('intervention', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='interventions.Intervention')),
                ('interventionset', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='interventions.InterventionSet')),
                ('output', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='interventions.Output')),
                ('outputset', models.ForeignKey(blank=True, null=True, on_delete=False, related_name='comments', to='interventions.OutputSet')),
            ],
        ),
    ]
