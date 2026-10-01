# Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

Sistema web desenvolvido para centralizar a gestão de pedidos, clientes e controle de estoque de bobinas e insumos para empresas de comunicação visual. A solução contempla cálculo de aproveitamento de material, baixa automatizada no estoque, entrada por código de barras e envio de notificações aos clientes via WhatsApp.

**Deploy:** Ainda não publicado — previsto para a Sprint 4  
**Equipe:** Breno Tales de Oliveira Leite (2840482423029) — Daniel Fredi Soares Pereira (2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

## Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python 3.10+ (Flask, Flask-SQLAlchemy)
- Banco de dados: SQLite 3 / PostgreSQL (SQLAlchemy ORM)

## Como rodar localmente
### Pré-requisitos
- Python 3.10 ou superior instalado ([python.org](https://www.python.org/))
- Git 2.30 ou superior instalado ([git-scm.com](https://git-scm.com/))

### Passo a passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/brenotales1/sistema-pedidos.git
   cd sistema-pedidos
   ```
2. Crie e ative o ambiente virtual (`.venv`):
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
     *(Caso o PowerShell bloqueie a execução de scripts, execute uma vez: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`)*
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente (copie `.env.example` para `.env` e preencha):
   | Variável | Descrição |
   |---|---|
   | `FLASK_APP` | Ponto de entrada da aplicação (`app.py`) |
   | `FLASK_ENV` | Ambiente de execução (`development` ou `production`) |
   | `SECRET_KEY` | Chave secreta de sessão Flask |
   | `DATABASE_URL` | URI de conexão do banco de dados |
5. Crie o banco e rode o schema:
   As tabelas e migrações são verificadas e criadas automaticamente na inicialização da aplicação (`app.py`). O schema DDL de referência está disponível em `database/schema.sql`.
6. Rode as migrations/seed (se houver):
   O seed inicial de materiais padrão é executado automaticamente na inicialização da aplicação (`app.py`).
7. Suba o projeto:
   ```bash
   python app.py
   ```
8. Acesse em `http://127.0.0.1:5000` (ou `http://localhost:5000`).

## Estrutura do repositório
```
/controllers     — Controladores (Blueprints) de rotas (clientes, estoque, pedidos)
/database        — Configuração de conexão do banco (db.py) e script DDL (schema.sql)
/docs            — Documentação técnica (DER, dicionário de dados, diagramas UML e capturas de tela)
/instance        — Arquivo do banco de dados SQLite local (database.db)
/models          — Modelos e entidades SQLAlchemy (Cliente, Pedido, Material, Bobina, etc.)
/services        — Regras de negócio, cálculo de aproveitamento, serviços de migração e seeds
/static          — Arquivos estáticos (CSS, imagens, scripts JS e uploads)
/templates       — Templates HTML renderizados pelo Jinja2
```

## Convenções da equipe
- Branches: `feature/nome-da-feature` para desenvolvimento, `develop` para integração e `main` para código estável.
- Commits: Padrão *Conventional Commits* (ex.: `feat: adiciona busca por codigo de barras`, `fix: corrige validacao de pedido`, `docs: atualiza readme`).
- Toda PR exige revisão de ao menos 1 integrante antes do merge.

## Testes
Como rodar: `python -m unittest discover -s tests -p "test_*.py"`

## Licença / Uso acadêmico
Projeto desenvolvido para a disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.
