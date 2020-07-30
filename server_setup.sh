: '
Assumptions:
you have ->
1. server (VPS)
2. Sudo user 
3. Login set up to server via ssh 
'

# Secure your server 

###########################################################

# $ sudo vi /etc/ssh/sshd_config
# -> Locate the line that starts with PermitRootLogin,PasswordAuthentication and
# change the value, whatever that might be in your server, to no.
# $ sudo service ssh restart

#############################################################

# Install firewall

$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
$ sudo ufw --force enable
$ sudo ufw status

# Install Base Dependencies

$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install mysql-server postfix supervisor nginx git


# These installations run mostly unattended, but at some point while you run 
# the third install statement you will be prompted to choose a root password for
# the MySQL service, and you ll also be asked a couple of questions regarding the
# installation of the postfix package which you can accept with their default 
# answers.


# Install the application 

git clone git@github.com:sid597/bolowiki.git
cd bolowiki
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
pip install gunicorn pymysql

################################################################
# IMPORTANT :
# Create a .env file and save all your secrets here one might consider changing
# the keys string different from the development. Because if the project is open
# source and I want it to be in prod then anyone could mess with session and stuff

################################################################

# Set up server for my app I am using MySql

mysql -u root -p

################################################################
# enter password which was set initially during installation
# Now in mysql create a new db call it whatever you want also create a user 
# with the same name that has full access to it

# mysql> create database something character set utf8 collate utf8_bin;
# mysql> create user 'something'@'localhost' identified by '<db-password>';
# mysql> grant all privileges on something.* to 'something'@'localhost';
# mysql> flush privileges;
# mysql> quit;

################################################################

flask db upgrade # Create db migration, Need to have flask migrate in app


# Setting Up Gunicorn and Supervisor


