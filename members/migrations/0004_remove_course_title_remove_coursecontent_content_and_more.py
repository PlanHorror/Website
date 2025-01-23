# Generated by Django 5.1.5 on 2025-01-22 08:43

import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_label_name_alter_project_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='title',
        ),
        migrations.RemoveField(
            model_name='coursecontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='label',
            name='name',
        ),
        migrations.RemoveField(
            model_name='news',
            name='title',
        ),
        migrations.RemoveField(
            model_name='newscontent',
            name='content',
        ),
        migrations.RemoveField(
            model_name='project',
            name='content',
        ),
        migrations.RemoveField(
            model_name='project',
            name='title',
        ),
        migrations.CreateModel(
            name='CourseContentTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('content', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.coursecontent')),
            ],
            options={
                'verbose_name': 'course content Translation',
                'db_table': 'members_coursecontent_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='CourseTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.course')),
            ],
            options={
                'verbose_name': 'course Translation',
                'db_table': 'members_course_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='LabelTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.TextField(unique=True, verbose_name='Name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.label')),
            ],
            options={
                'verbose_name': 'label Translation',
                'db_table': 'members_label_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='NewsContentTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('content', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.newscontent')),
            ],
            options={
                'verbose_name': 'news content Translation',
                'db_table': 'members_newscontent_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='NewsTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.news')),
            ],
            options={
                'verbose_name': 'news Translation',
                'db_table': 'members_news_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.TextField(verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='members.project')),
            ],
            options={
                'verbose_name': 'project Translation',
                'db_table': 'members_project_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
