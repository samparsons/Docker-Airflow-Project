from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
from datetime import datetime
from docker.types import Mount


dag = DAG('create_layers_in_snowflake',start_date=datetime.now(), schedule_interval=None,catchup=False)

run_dbt_task = DockerOperator(
    task_id='create_seeds',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    #command='sh -c "echo 1 && cd dbtlearn && dbt debug && echo 2 && cat dbt_project.yml && cd seeds && echo 3 && ls -l && cat full_moon_dates.csv"',
    #command='sh -c "ls -l && chmod -R 777 dbtlearn && ls -l && cd dbtlearn && ls -l && cd seeds && ls -l && cd /usr/app/ && dbt seed --project-dir /dbtlearn --profiles-dir /dbtlearn"',
    command='sh -c "dbt seed --project-dir ./dbtlearn --profiles-dir ./dbtlearn"',
    #auto_remove=True,
    mount_tmp_dir=False,
    network_mode='container:dbt',  
    dag=dag
)

run_dbt_task_1 = DockerOperator(
    task_id='create_target_layer',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    command='dbt run --models target_layer.*',
    #auto_remove=True,
    mount_tmp_dir=False,
    #mounts=[Mount(source='/Users/sparsons/Desktop/interview_test/Airflow_DBT_Snowflake_Docker/dbtlearn',target='/dbtlearn',type='bind')],
    network_mode='container:dbt',  
    dag=dag
)



run_dbt_task_2 = DockerOperator(
    task_id='create_business_layer',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    command='dbt run --models business_layer.*',
    auto_remove=True,
    mount_tmp_dir=False,
    #mounts=[Mount(source='./Users/sparsons/Desktop/interview_test/Airflow_DBT_Snowflake_Docker/dbtlearn',target='/dbtlearn',type='bind')],
    network_mode='container:dbt',  
    dag=dag
)

run_dbt_task_3 = DockerOperator(
    task_id='create_mart_full_moon',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    command='dbt run --models mart_full_moon_reviews.*',
    auto_remove=True,
    mount_tmp_dir=False,
    #mounts=[Mount(source='./Users/sparsons/Desktop/interview_test/Airflow_DBT_Snowflake_Docker/dbtlearn',target='/dbtlearn',type='bind')],
    network_mode='container:dbt',  
    dag=dag
)

run_dbt_task_4 = DockerOperator(
    task_id='create_mart_review_score',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    command='dbt run --models mart_review_score.*',
    auto_remove=True,
    mount_tmp_dir=False,
    #mounts=[Mount(source='./Users/sparsons/Desktop/interview_test/Airflow_DBT_Snowflake_Docker/dbtlearn',target='/dbtlearn',type='bind')],
    network_mode='container:dbt',  
    dag=dag
)

run_dbt_task_5 = DockerOperator(
    task_id='create_lineage_graph',
    image='custom_dbt_image',
    api_version='auto',
    docker_url='unix://var/run/docker.sock', 
    command='dbt docs generate && dbt docs serve --port 8085',
    mounts=[Mount(source='./Users/sparsons/Desktop/interview_test/Airflow_DBT_Snowflake_Docker/dbtlearn',target='/dbtlearn',type='bind')],
    network_mode='container:dbt',  
    dag=dag
)



#run_dbt_task_0 >> 
run_dbt_task >> run_dbt_task_1 >> run_dbt_task_2 >> [run_dbt_task_3,run_dbt_task_4] >> run_dbt_task_5