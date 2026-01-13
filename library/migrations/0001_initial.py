# Generated migration for Fase 1

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Author's full name", max_length=200)),
                ('country', models.CharField(blank=True, help_text='Country of origin (optional)', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Authors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text="Member's full name", max_length=200)),
                ('email', models.EmailField(help_text="Member's email (unique)", max_length=254, unique=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Book title', max_length=300)),
                ('isbn', models.CharField(help_text='ISBN code (unique)', max_length=20, unique=True)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('LOANED', 'Loaned'), ('LOST', 'Lost')], default='AVAILABLE', help_text='Current status of the book', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(help_text='Author of the book', on_delete=django.db.models.deletion.PROTECT, related_name='books', to='library.author')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loaned_at', models.DateTimeField(auto_now_add=True)),
                ('due_at', models.DateTimeField(help_text='Expected return date')),
                ('returned_at', models.DateTimeField(blank=True, help_text='Actual return date (null if not returned)', null=True)),
                ('book', models.ForeignKey(help_text='Book being loaned', on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='library.book')),
                ('member', models.ForeignKey(help_text='Member borrowing the book', on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='library.member')),
            ],
            options={
                'ordering': ['-loaned_at'],
            },
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['isbn'], name='library_boo_isbn_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['status'], name='library_boo_status_idx'),
        ),
        migrations.AddConstraint(
            model_name='loan',
            constraint=models.UniqueConstraint(condition=models.Q(('returned_at__isnull', True)), fields=('book',), name='unique_active_loan_per_book', violation_error_message='This book already has an active loan'),
        ),
    ]
