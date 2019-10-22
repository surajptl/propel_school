# Generated by Django 2.2.6 on 2019-10-22 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20191022_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='applicant',
            name='applicant_name',
            field=models.CharField(default=None, max_length=64),
        ),
        migrations.CreateModel(
            name='TaskPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=250, null=True)),
                ('joinedcandidates_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.JoinedCandidate')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TaskList')),
            ],
        ),
    ]
