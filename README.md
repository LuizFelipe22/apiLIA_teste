# empresasbr


## Criação dos containers


```
# Rede
docker network create lia_rede


docker run --name lia_database --network rede_lia --hostname lia_host1 -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=lia_bd -p 3306:3306 -d mysql:latest

docker cp backup.sql lia_database:/backup.sql

docker exec -it lia_database /bin/bash 
mysql -u root -p lia_bd < /backup.sql #Senha: 1234

# Saia do container: Ctrl + D


docker build -t api_lia:1.0 .

docker run -p 80:8000 --name lia_api --network rede_lia --hostname lia_host2 -d api_lia:1.0

```

- Após finalizar todos os comandos, digite:
    ```docker inspect lia_api```

- Procure o IP da api no tópico chamado "IPAddress"