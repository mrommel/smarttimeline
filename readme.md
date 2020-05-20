# SmartTimeline

project to 
- track app ratings and app releases
- monitor fritzbox
- display a project roadmap

## run the environment

cd ~/Prog/SmartTimeline/
source ~/.virtualenvs/smarttimeline/bin/activate
python3 manage.py runserver
deactivate

=> http://127.0.0.1:8000/timeline/dashboard


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

python3 manage.py makemigrations cms

## Links

https://demos.creative-tim.com/black-dashboard/examples/notifications.html