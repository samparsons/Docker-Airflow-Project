# Airflow
from airflow.models import DAG, Variable
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.decorators import task
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG




dag = DAG('test_questions',start_date=datetime.now(), schedule_interval=None,catchup=False)

#Create a new model, and create a yml to define a source.
task1 = BashOperator(
    task_id = 'bash1',
    bash_command = 'dbt build',
    dag=dag
)

#Create a new table or view that references the output of task1.
task2 = BashOperator(
    task_id = 'bash2',
    bash_command = 'ls',
    dag=dag
)


task1 >> task2