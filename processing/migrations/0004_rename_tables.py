from django.db import migrations

def rename_tables(apps, schema_editor):
    schema_editor.alter_db_table("", 'processing_collarbuttonsconfiguration',
                                 'male_configs_malecollarbuttonsconfiguration')
    schema_editor.alter_db_table("", 'processing_bodyconfiguration', 'male_configs_bodyconfiguration')
    schema_editor.alter_db_table("", 'processing_backconfiguration', 'male_configs_malebackconfiguration')
    schema_editor.alter_db_table("", 'processing_collarconfiguration', 'male_configs_malecollarconfiguration')
    schema_editor.alter_db_table("", 'processing_placketconfiguration', 'male_configs_placketconfiguration')
    schema_editor.alter_db_table("", 'processing_dickeyconfiguration', 'male_configs_dickeyconfiguration')
    schema_editor.alter_db_table("", 'processing_placketconfiguration_plackets',
                                 'male_configs_placketconfiguration_plackets')
    schema_editor.alter_db_table("", 'processing_bodyconfiguration_cuff_types',
                                 'male_configs_bodyconfiguration_cuff_types')


class Migration(migrations.Migration):
    dependencies = [
        ('processing', '0003_auto_20160824_2222'),
    ]

    operations = [
        migrations.RunPython(rename_tables),
    ]
