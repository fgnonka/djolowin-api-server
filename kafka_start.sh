
#!/bin/bash


# Activate your virtual environment
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; source ./djolowin-env/bin/activate; bash" &

# Start auction consumer
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; ./manage.py auction_consumer" &

#Start custom_user consumer
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; ./manage.py custom_user_consumer"