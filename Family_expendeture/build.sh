#!/usr/bin/env bash
# exit on error
set -o errexit

# সঠিক ডিরেক্টরি অনুযায়ী ইনস্টল করা
pip install -r Family_expendeture/requirements.txt

# স্ট্যাটিক ফাইল এবং মাইগ্রেশন রান করা
python Family_expendeture/manage.py collectstatic --no-input
python Family_expendeture/manage.py migrate