# Instruções para iniciar aplicação

## Gerar VENV

- `python -m venv venv --upgrade-deps`

## Entrar no VENV

- Linux/Mac - `source venv/bin/activate`
- Windows - `venv/Script/activate`

## Instalar dependências

- `pip install -r requirements.txt`

## Iniciar ambiente containerizado com Docker e Docker compose

- `sudo docker-compose up`

Caso dê problema com migrations antigas, rodar o comando:

- `sudo docker-compose down`
- `sudo docker volume ls`
- Remover o volume do docker antigo com: `sudo docker volume id_do_volume`
- rodar novamente o: `sudo docker-compose up`
