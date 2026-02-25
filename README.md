# Mensageiro

Sistema interno de comunicação por e-mail baseado em templates.

Permite que usuários criem templates padronizados e enviem mensagens para outros usuários do sistema, simulando o envio de e-mails internos.

---

## Funcionalidades

- Cadastro de usuários
- Login com autenticação JWT
- Criação de templates de e-mail
- Envio de mensagens usando templates
- Substituição de variáveis (ex: {{nome}})
- Caixa de entrada (mensagens recebidas)
- Histórico de mensagens enviadas e recebidas
- Frontend simples em HTML + JavaScript
- Execução via Docker

---

## Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLite
- Docker

---

## Executar localmente

### 1. Criar ambiente virtual

```
python -m venv venv
```

### 2. Ativar ambiente (Windows)

```
venv\Scripts\activate
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Executar aplicação

```
python app.py
```

Abrir no navegador:

```
http://localhost:5000
```

---

## Executar com Docker

Na pasta do projeto:

```
docker compose up --build
```

Abrir:

```
http://localhost:5000
```

Para parar:

```
docker compose down
```

---

## Como usar

1. Acesse o sistema
2. Cadastre um usuário
3. Faça login
4. Crie um template
5. Envie o template para outro usuário
6. Veja a mensagem na caixa de entrada

---

## Estrutura do projeto

```
Mensageiro/
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── templates/
│   ├── login.html
│   └── dashboard.html
└── instance/
```

---

## Rotas da API

### Públicas

Registro de usuário

POST /register

Body:

```
{
  "email": "user@email.com",
  "password": "123456"
}
```

---

Login

POST /login

Body:

```
{
  "email": "user@email.com",
  "password": "123456"
}
```

Retorna um token JWT.

---

### Privadas (requer autenticação)

Criar template

POST /templates

Body:

```
{
  "title": "Aviso",
  "subject": "Sistema fora do ar",
  "body": "Olá {{nome}}, o sistema estará indisponível."
}
```

---

Listar templates

GET /templates

---

Listar usuários

GET /users

---

Enviar mensagem

POST /send-email

Body:

```
{
  "template_id": 1,
  "receiver_id": 2,
  "nome": "Carlos"
}
```

---

Listar mensagens

GET /emails

---

## Observação

O envio de e-mail é simulado e armazenado no banco SQLite.

---

## Autor

José Vitor