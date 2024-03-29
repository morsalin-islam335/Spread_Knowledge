# Generated by Django 5.0 on 2024-02-23 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('balance_after_transaction', models.IntegerField()),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('borrow', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='borrowTransaction', to='book.borrow')),
            ],
        ),
    ]
