1. 셋업

   1. https://pipx.pypa.io/stable/installation/
   2. pipx install poetry
   3. poetry init
   4. poetry add django
   5. poetry shell
   6. django-admin startproject config .

2. 시작
   python manager.py runserver
   python manage.py migrate
   python manage.py createsuperuser

3. model 작성
   python manage.py startapp houses
   models 작성
   setting에 추가
   admin 작성
   python manage.py makemigrations
   python manage.py migrate

4. user
