
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import requests
import json

url_variables = "https://raw.githubusercontent.com/arturfc/docker-airflow-ETL-pipeline/main/datasets/variables_results.csv"
url_results = "https://raw.githubusercontent.com/arturfc/docker-airflow-ETL-pipeline/main/datasets/backtest_results.csv"

#ingesting variables input dataset
def variables_inputs():
    df_variables = pd.read_csv(url_variables, index_col=[0])
    df_variables = df_variables.to_json()
    return df_variables

#ingesting results dataset
def results_raw():
    df_results = pd.read_csv(url_results, index_col=[0])
    df_results = df_results.to_json()
    return df_results

#merging both datasets and transforming the data to a cleaner version
def results_clean(ti):
    df_variables = ti.xcom_pull(task_ids = 'variables_inputs')
    df_results = ti.xcom_pull(task_ids = 'results_raw')

    df_variables = pd.read_json(df_variables)
    df_results = pd.read_json(df_results)

    df_results.index.name = 'index'

    df_results_clean = pd.merge(df_results[['Saldo Líquido','Taxa de acerto']],
         df_variables[['results_index','RSI_enable','RSI_period','RSI_value']],
         how = "right", left_on=['index'], right_on=['results_index']).drop('results_index', 1)

    df_results_clean = df_results_clean.to_json()

    return df_results_clean

#refining data to get results that uses rsi indicator and contains specific conditions
def best_RSI_results(ti):
    df_results_clean = ti.xcom_pull(task_ids = 'results_clean')

    df_results_clean = pd.read_json(df_results_clean)

    df_best_RSI_results = df_results_clean.loc[(df_results_clean['RSI_enable'] == 1) &
                        (df_results_clean['Saldo Líquido'] > 500) &
                        (df_results_clean['Taxa de acerto'] > 0.60)].sort_values(by=['Saldo Líquido'], ascending=False)

    df_best_RSI_results = df_best_RSI_results.to_json()

    return df_best_RSI_results


with DAG ('dag_etl_best_strategy_results', start_date = datetime(2022,9,9),
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
