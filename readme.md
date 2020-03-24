# SmartTimeline

project to track app ratings and app releases

## run the environment
source ~/.virtualenvs/smarttimeline/bin/activate
python3 manage.py runserver
deactivate




## setup

###### create virtual env

python3 -m venv ~/.virtualenvs/smarttimeline

###### activate it

source ~/.virtualenvs/smarttimeline/bin/activate

###### deactivate it

deactivate

###### create new app

python3 manage.py startapp timeline

## migrations

python3 manage.py makemigrations timeline
python3 manage.py migrate

## Links

https://demos.creative-tim.com/black-dashboard/examples/notifications.html