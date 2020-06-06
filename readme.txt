I had this issue with not getting my environment variables being read in the app. This
issue was related to gunicorn, so to solve this issue I had to create a .env file and then
in my projects service file had to pass the EnvironmentFile path. This solved the issue


