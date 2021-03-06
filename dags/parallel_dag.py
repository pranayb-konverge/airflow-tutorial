from airflow import DAG
from airflow.operators.bash  import BashOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime
from subdags.subdag_parallel_dag import subdag_parallel_dag

default_args = {
    'start_date':datetime(2022,1,1),
}

with DAG('parallel_dag', 
        schedule_interval='@daily', 
        default_args=default_args, 
        catchup=False) as dag:
        
        task_1 = BashOperator(
            task_id='task_1',
            bash_command='sleep 3'
        )

        with TaskGroup('processing_task') as processing_task:
            task_2 = BashOperator(
                task_id='task_2',
                bash_command='sleep 3'
            )

            with TaskGroup('spark_task') as spark_task:
                task_3 = BashOperator(
                    task_id='task_3',
                    bash_command='sleep 3'
                )

            with TaskGroup('flint_task') as flint_task:
                task_3 = BashOperator(
                    task_id='task_3',
                    bash_command='sleep 3'
                )
            

        # this is a old and non recommended way of grouping the tasks. Use TaskGroup.
        # processing = SubDagOperator(
        #     task_id='processing_task',
        #     subdag=subdag_parallel_dag('parallel_dag','processing_task',default_args)
        # )

        task_4 = BashOperator(
            task_id='task_4',
            bash_command='sleep 3'
        )

        # task_1 >> processing >> task_4
        task_1 >> processing_task >> task_4