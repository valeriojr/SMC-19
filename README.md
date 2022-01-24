# Sistema de Coleta de Informações sobre o COVID-19

Ferramenta de coleta de dados.

[Quem somos](/projeto/covid-19_alagoas.pdf)

# Deploy
O deploy faz uso dos arquivos na pasta deploy:
- chaves ssl;
- arquivos com chaves secretas e senhas:
  * django-key (SECRET_KEY do django);
  * mysql-passwd (senha do root no MariaDB);
  * maps-api (API key do google maps);
caso precise alterar os arquivos acima, faça a edição na pasta deploy e rode o
build.

Utilize um dos métodos abaixo.

### Docker compose
Esquema dos containers:
    cliente web <--> nginx (smc19-nginx) <--> django com uwsgi (smc19) <--> mariadb (smc19-mariadb)

Build dos containers:
    docker-compose build

Rodando:
    docker-compose up

Rodadndo comandos no container do Django:
    docker exec -it smc19 python3 manage.py makemigrations
    docker exec -it smc19 python3 manage.py migrate
    docker exec -it smc19 python3 manage.py createsuperuser
    docker exec -it smc19 python3 manage.py cadastrar_unidades_cnes

### Vagrant
Os comandos são executados dentro da pasta Vagrant.

Criar as VMs:
    vagrant up

Instalar dependências e configurar tudo:
    ansible-playbook -i hosts smc19.yml
