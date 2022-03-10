# Generated by Django 4.0.1 on 2022-03-07 21:59


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('recycle', '0002_alter_dropofflocation_public_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=17, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('description', models.TextField()),
                ('approved', models.BooleanField(default=False, null=True)),
                ('still_available', models.BooleanField(default=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('zip_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recycle.zipcode')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=500)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reuse.post')),
            ],
        ),
    ]
