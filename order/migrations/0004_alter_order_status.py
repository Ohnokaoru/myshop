# Generated by Django 5.1 on 2024-08-28 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', '未付款'), ('completed', '付款完成'), ('cancelled', '取消')], max_length=20),
        ),
    ]
