# Generated by Django 3.2.13 on 2022-12-02 02:48

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_note_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stack',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Django', 'Django'), ('Spring', 'Spring'), ('Node.js', 'Node.js'), ('React', 'React'), ('MySQL', 'MySQL'), ('SQLite', 'SQLite')], default=1, max_length=40),
            preserve_default=False,
        ),
    ]