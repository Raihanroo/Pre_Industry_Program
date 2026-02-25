#!/usr/bin/env bash
# exit on error
set -o errexit

# সঠিক ফোল্ডারের ভেতরে গিয়ে ইনস্টল করা
pip install -r Family_expendeture/requirements.txt

# সঠিক পাথে manage.py রান করা
python Family_expendeture/manage.py collectstatic --no-input
python Family_expendeture/manage.py migrate