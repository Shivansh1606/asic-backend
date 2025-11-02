#!/bin/bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser if doesn't exist
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='root').exists():
    User.objects.create_superuser('root', 'root@asic.com', 'root123')
else:
    user = User.objects.get(username='root')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password('root123')
    user.save()
print("✅ User setup complete!")
END
