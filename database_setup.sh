#!/bin/bash
read -rp $'Enter username for db :' user 
read -rp $'Enter password for db :' password 
read -rp $'Enter database name  :' database
 
function execAsRoot() {

    command=${1}
    sudo mysql --user="root" --password=""  --execute="$command"
}

function execAsUser() {
    command=${1}
    sudo mysql --user="$user" --password="$password" --database="$database" --execute="$command"

}

execAsRoot "create database $database character set utf8 collate utf8_bin;"
execAsRoot "create user '$user'@'localhost' identified by '$password';"
execAsRoot "grant all privileges on $database.* to '$user'@'localhost';"
execAsRoot "flush privileges;"

source venv/bin/activate
export FLASK_APP=bolowikiApp/__init__.py
export FLASK_ENV=development      
flask db upgrade
