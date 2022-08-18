# <p align="center">[Pet CTRL - API](https://pet-ctrl-django.herokuapp.com/)</p>

##                          <p align="center">Esta API é o back-end da aplicação Pet-CTRL</p>
<br/>

<div align="center">Pet CTRL é uma aplicação que permite criar uma rede de pet shops. Nela, temos o controle sobre muitos aspectos da relação cliente - estabelicemento. Aqui nós temos a possibilidade de criar várias lojas com seus respectivos colaboradores, entre eles, os médicos veterinários que cuidarão da saúde do seu bichinho. 

A aplicação conta com a possibilidade de criar serviços e aplicar descontos individualmente. Contando com o cadastro de donos e pets, onde cada pet possui o seu próprio histórico de serviços e os preços , com ou sem desconto, de cada um deles.

A aplicação possui 46 rotas divididas em stores, staffs, services, services list (vinculado ao pet), pets, owners, e uma rota de login. Vale ressalta que todas as rotas exigem autenticação feita usando django authentication.

A URL base da Api é <a>https://pet-ctrl-django.herokuapp.com/</a>

Você pode ter acesso a documentação de todas as rotas por aqui <a>https://pet-ctrl-django.herokuapp.com/api/schema/swagger-ui/#/</a></div>    

<br/>
<br/>
<br/>

# <p align="center">Instruções para iniciar aplicação</p>

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
