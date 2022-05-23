from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash  import BashOperator

from datetime import datetime
import json
from pandas import json_normalize

default_args = {
    'start_date':datetime(2022,5,16),
}

def _processing_user(ti):
    users = ti.xcom_pull(task_ids=['extracting_user'])

    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty!')
    
    user = users[0]['results'][0]
    processed_user = json_normalize({
        "email": user['email'],
        "firstname": user['name']['first'],
        "lastname": user['name']['last'],
        "country": user['location']['country'],
        "username": user['login']['username'],
        "password": user['login']['password']
    })

    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)
#end of _processing_user method

with DAG('user_processing', 
        schedule_interval='@daily', 
        default_args=default_args, 
        catchup=False) as dag:

    # Define tasks/operators
    # task 1 - to create table using sqlite
    creating_table = SqliteOperator(
        task_id= 'creating_table',
        sqlite_conn_id='db_sqlite',
        sql= """
            CREATE TABLE IF NOT EXISTS users(
                email TEXT NOT NULL PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """
    )

    # task 2 - to create a http API sensor for connection
    # this step is to create REST API
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    # task 3 - to create a http operator to extract user data from sql table
    # the https://randomuser.me/ will get the result, we set this url in the connection on UI.
    extracting_user = SimpleHttpOperator(
        task_id= 'extracting_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response:json.loads(response.text),
        log_response=True
    )

    # task 4 - selecting specific information from the data and storing it in a CSV file.
    processing_user = PythonOperator(
        task_id='processing_user',
        python_callable=_processing_user # this method is defined up
    )

    # task 5 - store the data in CSV to the sqlite table `users`
    storing_user = BashOperator(
    task_id='storing_user',
    bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /home/airflow/airflow/airflow.db'
    )

    # create dependencies
    creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user