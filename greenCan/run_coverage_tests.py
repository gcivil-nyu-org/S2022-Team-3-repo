import os
os.chdir('./greenCan/')
os.system("python -m coverage run --source='.' manage.py test")