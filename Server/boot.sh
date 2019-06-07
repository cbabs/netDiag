#!/bin/sh
source venv/bin/activate

if [ $DEBUG = TRUE ];
then
  python ./netDiag/Server/manage.py runserver
else
  python ./netDiag/Server/startWebApp.py
fi


