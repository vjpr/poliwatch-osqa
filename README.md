#Poliwatch

##Ubuntu

Setting up a database in Ubuntu

    /opt/lampp/bin/mysql -u root
    mysql -u root -p
    CREATE USER 'rouesnel_pw'@'localhost' IDENTIFIED BY 'ASK VROUESNEL FOR PASSWORD';
    CREATE DATABASE rouesnel_pw DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci;

MySQL commands - http://www.pantz.org/software/mysql/mysqlcommands.html

##Production
Production database is hosted on webfaction
You can tunnel into it using putty
Change db to localhost:3306
Wont work with xampp in parallel
You can download it using phpmyadmin navicat through tunnelling
You can setup the database at any time by manage.py syncdb --all

###Taking a snapshot

    manage.py dumpdata > data.json

##Refreshing database after a model change

http://solutions.treypiepmeier.com/2008/09/28/use-django-fixtures-to-automatically-load-data-when-you-install-an-app/

You must have at least one user configured

    manage.py syncdb (answer 'no')
    manage.py reset forum (answer 'yes')
    manage.py loaddata data.json
    manage.py import_promises
    manage.py import_politicians

Assuming "c:\workspace-aptana\poliwatch\promise_data.csv" contains promises in this spreadsheet format

More info about migrating data: http://meta.osqa.net/questions/4080/how-can-i-import-data-from-another-question-and-answer-script

###Running the app

    manage.py runserver 0.0.0.0:8000

Sometimes you may have to run twice for it to start working
The additional IP allows it to be viewed over a private network

    Visit http://127.0.0.1:8000 or http://vaughan-pc:8000 remotely

##Deployment

Hosting: https://panel.webfaction.com/

Ask Vaughan for username and password.

Simply pull from bitbucket into /webapps/poliwatch/osqa/.

DB will need to be manually edited - use syncdb function to find out required changes.