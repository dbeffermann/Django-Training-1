# Generated migration for Fase 2

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Tag name (e.g., 'Fiction', 'Mystery', 'Science Fiction')", max_length=50, unique=True)),
                ('description', models.TextField(blank=True, help_text='Description of the tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MemberProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, help_text="Member's nickname (optional)", max_length=100, null=True)),
                ('risk_level', models.CharField(choices=[('LOW', 'Low Risk'), ('MED', 'Medium Risk'), ('HIGH', 'High Risk')], default='LOW', help_text='Risk level based on loan history', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('member', models.OneToOneField(help_text='Member profile (1:1 relationship, CASCADE deletion)', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='library.member')),
            ],
            options={
                'verbose_name_plural': 'Member Profiles',
            },
        ),
        migrations.CreateModel(
            name='BookTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(help_text='Book being tagged', on_delete=django.db.models.deletion.CASCADE, related_name='book_tags', to='library.book')),
                ('tag', models.ForeignKey(help_text='Tag applied to book', on_delete=django.db.models.deletion.CASCADE, related_name='book_tags', to='library.tag')),
            ],
            options={
                'verbose_name': 'Book Tag',
                'verbose_name_plural': 'Book Tags',
                'ordering': ['book', 'tag'],
            },
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('AVAILABLE', 'Available'), ('LOANED', 'Loaned'), ('LOST', 'Lost')], default='AVAILABLE', help_text='Current status of the book', max_length=20),
        ),
        migrations.AddConstraint(
            model_name='booktag',
            constraint=models.UniqueConstraint(fields=('book', 'tag'), name='unique_book_tag'),
        ),
    ]
