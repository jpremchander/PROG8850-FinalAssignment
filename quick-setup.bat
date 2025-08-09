@echo off
echo ==========================================
echo PROG8850 Database Automation - Quick Setup
echo ==========================================

echo.
echo Step 1: Starting MySQL Database...
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=Secret5555 -e MYSQL_DATABASE=project_db -p 3306:3306 mysql:8.0

echo.
echo Waiting 30 seconds for MySQL to start...
timeout /t 30 /nobreak

echo.
echo Step 2: Installing Python dependencies...
pip install mysql-connector-python

echo.
echo Step 3: Setting up database and tables...
mysql -h 127.0.0.1 -u root -pSecret5555 -e "CREATE DATABASE IF NOT EXISTS project_db;"
mysql -h 127.0.0.1 -u root -pSecret5555 project_db < sql/02_create_climate_table.sql
mysql -h 127.0.0.1 -u root -pSecret5555 project_db < sql/03_add_humidity_column.sql
mysql -h 127.0.0.1 -u root -pSecret5555 project_db < sql/04_seed_data.sql

echo.
echo Step 4: Verifying database setup...
mysql -h 127.0.0.1 -u root -pSecret5555 project_db -e "SELECT COUNT(*) as Total_Records FROM ClimateData;"
mysql -h 127.0.0.1 -u root -pSecret5555 project_db -e "DESCRIBE ClimateData;"

echo.
echo Step 5: Running concurrent query testing...
cd scripts
python multi_thread_queries.py
cd ..

echo.
echo ==========================================
echo Setup completed! 
echo.
echo Next steps for screenshots:
echo 1. Access database: mysql -h 127.0.0.1 -u root -pSecret5555 project_db
echo 2. View data: SELECT * FROM ClimateData LIMIT 10;
echo 3. Check containers: docker ps
echo.
echo Your system is ready for submission!
echo ==========================================
