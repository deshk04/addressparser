echo "Let's create django environment settings"
skey=`dd if=/dev/urandom bs=45 count=1 | base64`
echo "DJANGO_SECRET_KEY=$skey" > /addr/.env
cat /etc/environment >> ~/.bashrc
cd /addr/src/django/addr
# python manage.py runserver 0.0.0.0:8080
while true; do sleep 2; done
