#!/bin/bash

read -p "Enter package or service you want to install: " myvar

status2=$(yum list installed | grep "$myvar "| awk -F "." '{print $1}')

echo $myvar
echo $status2

if [ $status2==$myvar ] ; then
        echo "This package or service is already installed."
        exit 0;

else
        read -p "Would you like to install this package or service? " yn



fi
