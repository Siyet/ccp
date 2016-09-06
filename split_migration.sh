#! /bin/bash
echo "no" | python manage.py migrate processing 0004_rename_tables
echo "no" | python manage.py migrate male_configs --fake-initial
echo "no" | python manage.py migrate processing 0005_split_models_by_sex
echo "no" | python manage.py migrate processing 0006_remove_models_FAKE --fake
echo "yes" | python manage.py migrate