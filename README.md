# Airflow Tutorial
Tutorial Link - https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/

## Installation ond Airflow:
- `python3 -m venv sandbox`
- `source sandbox/bin/activate`
- `pip3 install wheel`
- `pip3 --no-cache-dir install apache-airflow==2.1.0 --constraint https://gist.githubusercontent.com/marclamberti/742efaef5b2d94f44666b0aec020be7c/raw/21c88601337250b6fd93f1adceb55282fb07b7ed/constraint.txt`

## Start Airflow:
- `airflow db init`
- `airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@airflow.com`

## Change default conf of sql_alchemy:
### By default the sqlite is configured but for parallel processing of task we cannot have sqlite, we will need postgres
- to check default conf - `airflow config get-value core sql_alchemy_conn` you will get "sqlite:////home/airflow/airflow/airflow.db"
- To use parallel processing the executor shoul be "LocalExecutor", to achive the same follow the commands.
- `sudo apt update`
- `sudo apt install postgresql`
- `sudo -u postgres psql`
    - `ALTER USER postgres PASSWORD 'postgres';`
- All Airflow features known to man - `pip install 'apache-airflow[all]'`
- `airflow db init`
- `pip install apache-airflow['cncf.kubernetes']`
- `airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@airflow.com`

## Install Elastic search
- `curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -`
    - password is airflow
- `echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list`
- `sudo apt update && sudo apt install elasticsearch`
- `pip install elasticsearch==7.10.1`
- Start Elasticsearch with - `sudo systemctl start elasticsearch`
- Check if Elasticsearch works with - `curl -X GET 'http://localhost:9200'`

# Use docker-compose for running Airflow in multiple containers locally without Virtual Machine.
Please check the README.md file inside the `airflow-local` folder.
