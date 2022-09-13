
# *Airflow* com *docker compose* para criação de pipelines ETL

<imagem aqui (gif do processo sendo executado time sleep 1)>

#### Overview
Dados são capturados em tempo real para orquestração dos processos ETL,
 utilizando *docker-compose* para administração de um ambiente isolado (apenas configurações necessárias),
  permitindo a utilização do *Airflow* para o gerenciamento de fluxo de trabalho.

### ETL **DAG** flow utilizado
- Extração de dois datasets com chaves em comum, contendo registros de estratégias de mercado financeiro (explicado em <link>).
- Transformação dos dados, obtendo apenas as informações necessárias para o produto final.
- Refinamento dos dados para rankear apenas registros que possuem o indicator de *RSI* ativado, taxa de acerto acima de 60% e saldo líquido acima de 500 reais.

## Setup do ambiente
Será utilizado o docker para obter a instalação enxuta do *Airflow*.
### Docker
Instalação do docker é bem direta, basta efetuar o [download](https://www.docker.com/) e realizar a isntalação padrão.
### Docker-compose
Para usuários de Windows e MAC, o docker-compose já foi instalado automaticamente no passo anterior. Para usuários de Linux, é necessário aplicar os seguintes comandos:

```bash
  sudo apt-get update
  sudo apt-get install docker-compose-plugin
```

O arquivo [docker-compose.yaml](https://github.com/arturfc/docker-airflow-ETL-pipeline/blob/main/docker-compose.yaml) precisa ser inserido no diretório do projeto, juntamente com as pastas **dags**, **logs** e **plugins**.

## Setup do *Airflow*
Será criado a estrutura dentro do container para a utilização do *Airflow*. No diretório do projeto, execute:

```bash
  docker-compose up airflow-init
```
Para a inicialização do *Airflow* em seu localhost, execute:

```bash
  docker-compose up
```
Após inicializado, por padrão, será possível acessar o http://localhost:8080/home com senha e login **airflow**.

Para finalizar o docker, basta executar:

```bash
  docker-compose down
```

## Como rodar as DAGs dentro do airflow
