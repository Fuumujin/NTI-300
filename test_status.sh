#!/bin/bash

myvar=""

if [ -z "$1" ] ; then
  echo "you didn't provide an argument"
  exit 0;
fi

status=$(systemctl status httpd | grep Active | awk '{print $2}') 
inactive="inactive" 

if [ $status == $inactive ]; then 
	echo "noooo it's off"; 
else
	echo "My status is $status"

fi
