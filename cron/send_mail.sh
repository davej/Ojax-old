# cheat and hard-code the path.
PROJECT_ROOT=/home/dave/public_html/ojaxvre
 
# activate the oebfare virtualenv
. /home/dave/sources/pinax-env/bin/activate
 
cd $PROJECT_ROOT
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1