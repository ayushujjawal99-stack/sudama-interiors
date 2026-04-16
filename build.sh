#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Migrations
python manage.py makemigrations services
python manage.py migrate services
python manage.py migrate

# Create admin if needed
if [ "$CREATE_SUPERUSER" = "1" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

user, created = User.objects.get_or_create(username="admin")
user.set_password("admin12345")
user.is_staff = True
user.is_superuser = True
user.save()

print("Admin created or updated")
END
fi

# 🔥 FIX: Reset static files properly
rm -rf staticfiles || true
python manage.py collectstatic --no-input