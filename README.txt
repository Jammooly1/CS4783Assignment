Members:
Jamal Dabas, iuq276
Majd Hamoudah, hww134

We used a python library called mysqldb

Commands:

pip3 install mysqlclient
pip install pyopenssl
pip3 install flask_swagger_ui

Instructions:

When adding the api KEY, add X-Api-Key=<key> as a header
To access swagger ui just type /swagger
when running the program add pram http or https

when running in pm2 run following commands:
export FLASK_APP=app.py
pm2 start "flask run -p 12100" -- https or http



Github:

https://github.com/Jammooly1/CS4783Assignment
