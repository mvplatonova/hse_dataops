"""
Example Airflow DAG
Демонстрация базовых возможностей Airflow
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Python function for PythonOperator
def print_hello():
    """Simple Python function"""
    print("Hello from Airflow!")
    return "Success"

def print_context(**context):
    """Print execution context"""
    print(f"Execution date: {context['ds']}")
    print(f"DAG: {context['dag']}")
    return "Context printed"

# Define DAG
with DAG(
    dag_id='example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example', 'tutorial'],
) as dag:
    
    # Task 1: Start
    start = DummyOperator(
        task_id='start',
    )
    
    # Task 2: Bash command
    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "Running Bash command"',
    )
    
    # Task 3: Python function
    python_task = PythonOperator(
        task_id='python_task',
        python_callable=print_hello,
    )
    
    # Task 4: Python with context
    context_task = PythonOperator(
        task_id='context_task',
        python_callable=print_context,
        provide_context=True,
    )
    
    # Task 5: Another bash task
    final_bash = BashOperator(
        task_id='final_bash',
        bash_command='echo "Pipeline completed successfully"',
    )
    
    # Task 6: End
    end = DummyOperator(
        task_id='end',
    )
    
    # Define task dependencies
    # Linear flow: start -> bash_task -> python_task -> context_task -> final_bash -> end
    start >> bash_task >> python_task >> context_task >> final_bash >> end
