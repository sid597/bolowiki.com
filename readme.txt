I had this issue with not getting my environment variables being read in the app. This
issue was related to gunicorn, so to solve this issue I had to create a .env file and then
in my projects service file had to pass the EnvironmentFile path. This solved the issue

Issue : MySQLdb not found
Suggested ->
Solution 1 : First do pip install -U setuptools  --result--> Did not work
Solution 2 : sudo python3 -m pip install mysql-connector
                --result--> NOPE

solution 3 : sudo apt-get install python3-dev libmysqlclient-dev
                 --result--> NOPE

