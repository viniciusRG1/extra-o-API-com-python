from airflow import DAG
from datetime import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator

from pokemon import extractPokemon


default_args = {
    'owner': 'vinicius',
    "start_date": datetime(2026, 3, 17),
}

dag = DAG(
    "extractPokemon",
    default_args=default_args,
    schedule="0 10 * * *",
    max_active_runs=1,
)

start_pipeline = PythonOperator(task_id='startPipeline',python_callable=extractPokemon, dag=dag)

extract_pokemon = PythonOperator(
    task_id='extractPokemon',
    python_callable=extractPokemon,
    dag=dag
)

done_pipeline = EmptyOperator(
    task_id='donePipeline',
    dag=dag
)

start_pipeline >> extract_pokemon >> done_pipeline