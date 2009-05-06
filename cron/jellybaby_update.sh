# cheat and hard-code the path.
PROJECT_ROOT=/home/dave/public_html/ojaxvre
 
# activate the oebfare virtualenv
. /home/dave/sources/pinax-env/bin/activate
 
cd $PROJECT_ROOT
python manage.py jellybaby_update >> $PROJECT_ROOT/logs/jellybaby_update.log 2>&1