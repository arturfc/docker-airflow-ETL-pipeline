import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
#from airflow.operators.bash import BashOperator
from datetime import datetime


#ingesting variables_input dataset
def variables_inputs():
    df_variables = pd.read_csv("variables_results.csv", index_col=[0])
    return df_variables

#ingesting results dataset
def results_raw():
    df_results = pd.read_csv("backtest_results.csv", index_col=[0])
    df_results.index.name = 'index'
    return df_results


def results_clean(ti): #ti
    df_variables = ti.xcom_pull(task_ids = 'variables_inputs')
    df_results = ti.xcom_pull(task_ids = 'results_raw')

    df_results_clean = pd.merge(df_results[['Saldo Líquido','Taxa de acerto']],
         df_variables[['results_index','RSI_enable','RSI_period','RSI_value']],
         how = "right", left_on=['index'], right_on=['results_index']).drop('results_index', 1)

    return df_results_clean


def best_RSI_results(ti):
    df_results_clean = ti.xcom_pull(task_ids = 'results_clean')

    df_best_RSI_results = df_results_clean.loc[(df_results_clean['RSI_enable'] == 1) &
                        (df_results_clean['Saldo Líquido'] > 500) &
                        (df_results_clean['Taxa de acerto'] > 0.60)].sort_values(by=['Saldo Líquido'], ascending=False)

    return df_best_RSI_results


with DAG ('dag_example_results', start_date = datetime(2022,9,9),
            schedule_interval = '30 * * * *', catchup = False) as dag: 

    variables_inputs = PythonOperator(
        task_id = 'variables_inputs',
        python_callable = variables_inputs
    )

    results_raw = PythonOperator(
        task_id = 'results_raw',
        python_callable = results_raw
    )

    results_clean = PythonOperator(
        task_id = 'results_clean',
        python_callable = results_clean
    )

    best_RSI_results = PythonOperator(
        task_id = 'best_RSI_results',
        python_callable = best_RSI_results
    )

    [variables_inputs,results_raw] >> results_clean >> best_RSI_results
