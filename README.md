# Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

Sistema web para gerenciar clientes, pedidos, estoque de bobinas e notificações pelo WhatsApp.

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto<br>
**Deploy definitivo:** https://center-pedidos.onrender.com<br>
**Repositório:** https://github.com/brenotales1/sistema-pedidos<br>
**Consolidação E10:** 15/11/2026 · entrega online até 20/11/2026, às 23h59.

## Documentação

- [Documentação final consolidada — E10](docs/documentacao-final.md): índice E1–E9, desvios, arquitetura e rastreabilidade.
- [Manual do usuário](docs/manual-do-usuario.md): operação por perfil.
- [Situação da entrega E10](docs/E10-README.md).
- [Relatório final de testes — E9](docs/relatorio-testes-final.md).
- [Termo de aceite do cliente — E9b](docs/E9-termo-de-aceite-cliente.md).

## Funcionalidades

- Autenticação com perfis Administrador e Funcionário.
- Cadastro, busca, identificação e entrada de materiais por código de barras.
- Controle de bobinas, saldo em metros, estoque mínimo e histórico de movimentações.
- Cadastro de clientes, cálculo de aproveitamento e gestão de pedidos com vários materiais por pedido (relação N:N por ConsumoMaterial).
- Notificação automática ao mudar o pedido para **Pronto para retirada**.
- Histórico administrativo de tentativas de notificação, com filtros e paginação.

O recebimento real da notificação do pedido #3 está documentado na [captura da E9](docs/screenshots/whatsapp-pedido-3.png). O aceite da API e a entrega ao destinatário são registros diferentes; o webhook atual recebe eventos, mas não atualiza automaticamente a confirmação de entrega no banco.

## Tecnologias

| Camada | Implementação |
|---|---|
| Interface | HTML, CSS, JavaScript e templates Jinja2 |
| Aplicação | Python, Flask 3.1.3 e Blueprints |
| Persistência | Flask-SQLAlchemy; SQLite por padrão local; conexão configurável por DATABASE_URL |
| Integração | Meta WhatsApp Cloud API, requests e phonenumbers |
| Execução em produção | Gunicorn; aplicação hospedada no Render |

As dependências estão em [requirements.txt](requirements.txt). O banco de dados do projeto é SQLite. Conforme informado pelo responsável, o banco local não foi migrado para o Render.

## Como rodar localmente

Use Python 3.12 para reproduzir o ambiente documentado nos testes, além de Git.

1. Clone e entre no repositório:

   ```powershell
   git clone https://github.com/brenotales1/sistema-pedidos.git
   cd sistema-pedidos
   ```

2. Crie o ambiente virtual e instale as dependências:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Copie a configuração de exemplo e ajuste os valores:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Inicie a aplicação:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

5. Acesse http://127.0.0.1:5000 e faça login.

No Linux/macOS, use `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, `cp .env.example .env` e `python app.py`.

A inicialização aplica as migrações da aplicação, cria as tabelas e prepara os materiais iniciais. A migração ConsumoMaterial associa os pedidos antigos a materiais identificáveis sem baixar novamente o estoque; faça backup do SQLite antes de iniciar esta versão sobre dados existentes. Em banco sem usuários, cria as contas locais abaixo; `python criar_usuario.py` também permite criar as contas ausentes.

| Perfil de demonstração local | E-mail | Senha inicial |
|---|---|---|
| Administrador | admin@sistema.com | 123456 |
| Funcionário | funcionario@sistema.com | 123456 |

Essas são contas de demonstração local. Antes de expor o serviço, defina credenciais próprias; não dependa das contas padrão em produção. O comando `python app.py` executa o servidor de desenvolvimento com debug.

## Configuração

Não versione o arquivo `.env` nem compartilhe tokens.

| Variável | Uso |
|---|---|
| SECRET_KEY | Chave de sessão; definir valor próprio em produção |
| DATABASE_URL | Conexão SQLAlchemy; padrão local sqlite:///database.db |
| WHATSAPP_ENABLED | false para execução sem mensagens reais; true habilita a integração configurada |
| META_PHONE_NUMBER_ID | Identificador do número remetente na Meta |
| META_ACCESS_TOKEN | Token de acesso à integração |
| META_TEMPLATE_NAME | Nome do template aprovado; exemplo: pedido_finalizado |
| META_TEMPLATE_LANG | Idioma do template; exemplo: pt_BR |
| META_VERIFY_TOKEN | Valor próprio para validar a inscrição do webhook |

`FLASK_APP` e `FLASK_ENV` constam do exemplo de ambiente; o comando direto usa `app.py`, que define o modo de desenvolvimento no código.

Para envio real, configure as credenciais, o template aprovado e um destinatário válido. O disparo acontece na transição para **Pronto para retirada**; repetir o mesmo status não gera nova tentativa. A atualização do pedido é preservada mesmo quando o envio falha.

O endereço de webhook é `https://center-pedidos.onrender.com/webhook/whatsapp`. A inscrição usa `META_VERIFY_TOKEN`. O código atual valida a inscrição por GET e recebe eventos por POST; não associa esses eventos à confirmação de entrega das notificações.

## Execução em produção

O [Procfile](Procfile) contém o comando:

```text
gunicorn "app:create_app()"
```

Instale as dependências com `pip install -r requirements.txt` e configure as variáveis no serviço. Para SQLite, o arquivo precisa ficar em armazenamento persistente; alternativamente, configure uma conexão de banco persistente por `DATABASE_URL`. O repositório inclui o driver PostgreSQL, mas isso não confirma seu uso no deploy atual.

## Testes

No PowerShell:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

A bateria original da E9 registrou **115 testes aprovados**. Após a implementação N:N na E10, a suíte atual executou **131 testes aprovados**: os 115 anteriores e 16 novos testes de consumo, migração e integridade. Consulte a [validação N:N](docs/E10-validacao-nn.md) e o [log](docs/E10-testes-nn.txt). Os testes de integração externa usam mocks, e a cobertura de linhas/branches não foi mensurada. Consulte o [plano atualizado](docs/plano-de-testes.md) e o [relatório final](docs/relatorio-testes-final.md).

## Estrutura

| Diretório / arquivo | Responsabilidade |
|---|---|
| app.py | Criação da aplicação, configuração, inicialização e webhook |
| controllers/ | Rotas, sessão e autorização |
| services/ | Estoque, materiais, pedidos, WhatsApp e migrações |
| models/ | Entidades SQLAlchemy |
| database/ | Conexão e referência SQL |
| templates/ e static/ | Telas, estilos e scripts |
| tests/ | Testes unitários e de integração |
| docs/ | Artefatos E1–E10, manual e evidências |
| instance/ | Banco SQLite local, quando utilizada a configuração padrão |

## Como contribuir

1. Crie uma branch `feature/nome-da-feature` a partir da branch de integração `develop`.
2. Implemente a alteração e os testes necessários para novas regras.
3. Execute a suíte e atualize os documentos afetados.
4. Abra um PR para revisão de pelo menos outro integrante antes do merge.

Usamos Conventional Commits, por exemplo `feat: adiciona filtro`, `fix: corrige saldo` e `docs: atualiza manual`. A branch `main` representa o código estável.

## Uso acadêmico

Projeto da disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.

## Pedidos com vários materiais

No formulário, selecione o material principal para o cálculo de corte. Use **+ Adicionar material** para incluir materiais adicionais e informe o consumo total em metros de cada um. Um material não pode se repetir no mesmo pedido. Os adicionais são consumos em metros, sem cálculo de corte próprio.

A edição devolve os consumos anteriores e aplica os novos; o cancelamento permitido estorna todos os materiais. O detalhe lista as associações. A implementação está em [ConsumoMaterial](models/consumo_material.py), o modelo final em [DER](docs/der.md) e o DDL atual em [database/schema.sql](database/schema.sql).

A nova funcionalidade foi implementada e testada localmente. Para utilizá-la no Render, publique esta versão e atualize a captura do formulário no manual. O aceite histórico da E9 não foi ampliado automaticamente para essa mudança.
