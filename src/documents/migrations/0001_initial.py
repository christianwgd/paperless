# Generated by Django 3.1.1 on 2020-09-10 19:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correspondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, editable=False, verbose_name='Slug')),
                ('match', models.CharField(blank=True, max_length=256, verbose_name='Match')),
                ('matching_algorithm', models.PositiveIntegerField(choices=[(1, 'Any'), (2, 'All'), (3, 'Literal'), (4, 'Regular Expression'), (5, 'Fuzzy Match')], default=1, help_text='Which algorithm you want to use when matching text to the OCR\'d PDF.  Here, "any" looks for any occurrence of any word provided in the PDF, while "all" requires that every word provided appear in the PDF, albeit not in the order provided.  A "literal" match means that the text you enter must appear in the PDF exactly as you\'ve entered it, and "regular expression" uses a regex to match the PDF.  (If you don\'t know what a regex is, you probably don\'t want this option.)  Finally, a "fuzzy match" looks for words or phrases that are mostly—but not exactly—the same, which can be useful for matching against documents containg imperfections that foil accurate OCR.', verbose_name='Matching algorithm')),
                ('is_insensitive', models.BooleanField(default=True, verbose_name='is_insensitive')),
            ],
            options={
                'verbose_name': 'Correspondent',
                'verbose_name_plural': 'Correspondents',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.UUIDField(blank=True, verbose_name='Group')),
                ('message', models.TextField(verbose_name='Message')),
                ('level', models.PositiveIntegerField(choices=[(10, 'Debugging'), (20, 'Informational'), (30, 'Warning'), (40, 'Error'), (50, 'Critical')], default=20, verbose_name='Level')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
                'ordering': ('-modified',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, editable=False, verbose_name='Slug')),
                ('match', models.CharField(blank=True, max_length=256, verbose_name='Match')),
                ('matching_algorithm', models.PositiveIntegerField(choices=[(1, 'Any'), (2, 'All'), (3, 'Literal'), (4, 'Regular Expression'), (5, 'Fuzzy Match')], default=1, help_text='Which algorithm you want to use when matching text to the OCR\'d PDF.  Here, "any" looks for any occurrence of any word provided in the PDF, while "all" requires that every word provided appear in the PDF, albeit not in the order provided.  A "literal" match means that the text you enter must appear in the PDF exactly as you\'ve entered it, and "regular expression" uses a regex to match the PDF.  (If you don\'t know what a regex is, you probably don\'t want this option.)  Finally, a "fuzzy match" looks for words or phrases that are mostly—but not exactly—the same, which can be useful for matching against documents containg imperfections that foil accurate OCR.', verbose_name='Matching algorithm')),
                ('is_insensitive', models.BooleanField(default=True, verbose_name='is_insensitive')),
                ('colour', models.PositiveIntegerField(choices=[(1, '#a6cee3'), (2, '#1f78b4'), (3, '#b2df8a'), (4, '#33a02c'), (5, '#fb9a99'), (6, '#e31a1c'), (7, '#fdbf6f'), (8, '#ff7f00'), (9, '#cab2d6'), (10, '#6a3d9a'), (11, '#b15928'), (12, '#000000'), (13, '#cccccc')], default=1, verbose_name='Color')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, max_length=128)),
                ('content', models.TextField(blank=True, db_index=True, help_text='The raw, text-only data of the document. This field is primarily used for searching.')),
                ('file_type', models.CharField(choices=[('pdf', 'PDF'), ('png', 'PNG'), ('jpg', 'JPG'), ('gif', 'GIF'), ('tiff', 'TIFF'), ('txt', 'TXT'), ('csv', 'CSV'), ('md', 'MD')], editable=False, max_length=4)),
                ('checksum', models.CharField(editable=False, help_text='The checksum of the original document (before it was encrypted).  We use this to prevent duplicate document imports.', max_length=32, unique=True)),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('storage_type', models.CharField(choices=[('unencrypted', 'Unencrypted'), ('gpg', 'Encrypted with GNU Privacy Guard')], default='unencrypted', editable=False, max_length=11)),
                ('added', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('filename', models.FilePathField(default=None, editable=False, help_text='Current filename in storage', max_length=256, null=True)),
                ('correspondent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='documents.correspondent')),
                ('tags', models.ManyToManyField(blank=True, related_name='documents', to='documents.Tag')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
                'ordering': ('correspondent', 'title'),
            },
        ),
    ]
