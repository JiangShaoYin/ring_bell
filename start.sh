nohup python3 ring_bell.py &
echo $? > pid.txt
ps -elf | grep /usr/local/Cella
kill -9 34534
