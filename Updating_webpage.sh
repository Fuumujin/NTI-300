#1/bin/bash
time=$(date)                                                                                              #sets variable time
echo "<html><body><h1>Hi there, it is $time, how are you?</h1></body></html>" > /var/www/html/index.html  #creates custom message
