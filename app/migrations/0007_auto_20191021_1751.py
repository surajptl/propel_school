# Generated by Django 2.2.6 on 2019-10-21 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20191021_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='applicant_name',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='d_o_b',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='fcc_eligible',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='fcc_link',
            field=models.CharField(default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='interest',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='job_state',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='phone_number',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='propel_mode',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
    ]
