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

4. 관리자 패널에서 데이터 확인
   python manager.py shell
   >>> from rooms.models import Room
   >>> Room.objects
   <django.db.models.manager.Manager object at 0x10db3c710>
   >>> Room.objects.all()
   <QuerySet [<Room: 아름다운 내집>]>
   >>> room = Room.objects.get(name='아름다운 내집')
   >>> room
   <Room: 아름다운 내집>
   >>> room.pk
   1
   >>> room.id
   1
   >>> room
   <Room: 아름다운 내집>
   >>> room.name
   '아름다운 내집'
   >>> room.owner
   <User: deepplin>
   >>> room.price
   300
   >>> room.price = 200
   >>> room.save()
   >>> room
   <Room: 아름다운 내집>
   >>> room.price
   200
   >>> room.amenities.all()
   <QuerySet [<Amenity: 에어컨>]>
   >>> Room.objects.filter(name__contains='아름')
   <QuerySet [<Room: 아름다운 내집>]>
   >>> Room.objects.filter(price__gt=200)
   <QuerySet []>
   >>> Room.objects.filter(price__gt=100)
   <QuerySet [<Room: 아름다운 내집>]>
   >>> from rooms.models import Amenity
   >>> Amenity.objects.all()
   <QuerySet [<Amenity: 에어컨>]>
   >>> Amenity.objects.create(name='Console', description='box is good')
   <Amenity: Console>
   >>> Amenity.objects.all()
   <QuerySet [<Amenity: 에어컨>, <Amenity: Console>]>