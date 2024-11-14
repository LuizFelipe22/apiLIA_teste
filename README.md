# empresasbr


## Criação dos containers


```
# Rede
docker network create lia_rede


docker run --name lia_database --network lia_rede --hostname lia_host1 -e MARIADB_ROOT_PASSWORD=1234 -e MARIADB_DATABASE=lia_bd -p 3306:3306 -d mariadb:latest

docker cp backup.sql lia_database:/backup.sql

docker exec -it lia_database /bin/bash 
mariadb -u root -p lia_bd < /backup.sql #Senha: 1234

# Saia do container: Ctrl + D


docker build -t api_lia:1.0 .

docker run -p 8000:8000 --name lia_api --network lia_rede --hostname lia_host2 -d api_lia:1.0

```

- Após finalizar todos os comandos, digite:
    ```docker inspect lia_api```

- Procure o IP da api no tópico chamado "IPAddress" ou acesse a aplicação no host `localhost:8000/docs`