# livraria-online

### 👉 Instalação em ambiente linux

> Instale os mudulos em uma máquina virtual `VENV`

```bash

$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python manage.py migrate

> Com um banco postgres criado, aponte seu arquivo .env para um banco existente
> por exemplo : DATABASE_URL=postgres://postgres:postgres@localhost:5432/livraria-online


> Rode o comando abaixo para popular o banco com a api dos livros

$ python manage.py fetch_books
$ python manage.py runserver

# livraria-online-tsmx
# livraria-online-tsmx
