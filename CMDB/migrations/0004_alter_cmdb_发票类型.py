# Generated by Django 4.0.6 on 2022-07-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMDB', '0003_rename_detail_cmdb_明细_rename_amount_cmdb_金额_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmdb',
            name='发票类型',
            field=models.CharField(blank=True, choices=[('截图', '截图'), ('发票', '发票'), ('截图+发票', '截图+发票')], max_length=255, null=True),
        ),
    ]
