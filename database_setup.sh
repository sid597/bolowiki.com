sudo mysql -u root -p
read -rp $'Enter username for db :' user 
read -rp $'Enter password for db :' password 
read -rp $'Enter database name  :' database
    
function execInMySQL() {
    command=${1}
    sudo mysql --user="$user" --password="$password" --database="$database" --execute="$command"
}

execInMySQL "create database $database character set utf8 collate utf8_bin;"
execInMySQL "create user '$user'@'localhost' identified by '';"
execInMySQL "grant all privileges on $database.* to '$user'@'localhost';"
execInMySQL "flush privileges;"
execInMySQL "quit;"

flask db upgrade
