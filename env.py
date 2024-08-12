"""
This module sets environment variables for the Django project.

It includes configurations such as the secret key, debug mode,
allowed hosts, and the database URL. These settings are essential
for the secure and proper functioning of the Django application.
"""

import os

os.environ["SECRET_KEY"] = 'django-insecure-8us@c&7q&bdifzq(g7dpfj=#wgs&$6tc82zi1@$rjla7enqb=+'
os.environ["DEBUG"] = 'True'
os.environ["ALLOWED_HOST"] = "vetappt-9a4ac7bc1416.herokuapp.com"
os.environ["DATABASE_URL"] = 'postgres://ufheva6h8rl839:pe1abbdc02a6d1eefa98a101c4ab3b1a8d88fde8c4238ce993f6a72bdea245f17@c1i13pt05ja4ag.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/daj7mk92jsmhkn'
