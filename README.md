# Persistência Poliglota de Dados

Aplicação de biblioteca de animes utilizando banco de dados Redis, Neo4j e utilizando Spark para extração e tratamento de dados

## Comandos

### Para colocar no ar

Execute o comando: 

docker-compose up

### Para desligar o servidor

Execute os comandos:

docker stop $(docker ps -a -q)

docker rm $(docker ps -a -q)
