# Roteiro do Protótipo Navegável — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto.

**Link do protótipo:** https://www.figma.com/make/CITmJdPdYf8afoMoqX9TLM/prototipo-API?t=pnjhPEgDFrhV7bCw-20&fullscreen=1

---

## 1. Escopo do Protótipo e Telas do Sistema

Como o nosso projeto partiu de um sistema base já existente (Trilha A), as funções básicas de Login (#1), Cadastro de materiais (#2) e Consulta de estoque (#3) já estavam implementadas no sistema. Por esse motivo, o protótipo navegável no Figma foca nas **novas funcionalidades desenvolvidas no semestre** (leitura por código de barras, notificações via WhatsApp e histórico de disparos).

As telas do sistema base podem ser conferidas diretamente na aplicação em execução ou nas capturas presentes na pasta `docs/screenshots/`.

Abaixo estão as telas do incremento representadas no protótipo:

| Tela / Componente | Perfil | História relacionada (E2) | O que a tela mostra / permite |
|---|---|:---:|---|
| **1. Identificação e entrada por código de barras** | Funcionário | #4, #5 | Campo para bipar ou digitar o código, identificação do material e confirmação de entrada de bobinas no estoque |
| **2. Modal de notificação WhatsApp** | Funcionário | #7, #8, #9 | Após atualizar o pedido, exibe dados do cliente e prévia da mensagem com opção de confirmar ou cancelar o envio |
| **3. Feedback do envio (Toast/Alerta)** | Funcionário | #8, #9 | Notificação visual em tela informando o resultado imediato do envio da API (sucesso com mensagem enviada ou aviso de falha) |
| **4. Histórico de notificações enviadas** | Administrador | #10 | Tabela de auditoria com cliente, pedido, telefone, data/hora e status do envio (*enviada* ou *falha*) |

---

## 2. Detalhamento dos frames do protótipo

### Frame 1 — Entrada de material por código de barras
- **Cabeçalho:** "Entrada de Material no Estoque".
- **Campo de entrada:** `[ Bipar ou digitar código de barras... ]` com ícone de leitor.
- **Card de retorno:** Quando o código é lido, exibe:
  - Material: Lona Branca Brilho 3.20m
  - Categoria: Lona | Código: `7890000000011`
  - Estoque atual: 50.0m
- **Quantidade:** Campo numérico para informar a quantidade de metros recebidos.
- **Ação principal:** Botão `[ Confirmar Entrada ]`.
- **Resultado esperado:** Confirmar a entrada e atualizar o saldo do estoque após validar o código e a quantidade.

### Frame 2 — Confirmação de notificação WhatsApp
- **Título:** "Deseja enviar notificação ao cliente via WhatsApp?".
- **Contexto:** Modal exibido na tela de pedidos após atualizar o status.
- **Dados do cliente:** João Silva — `(11) 99999-9999`.
- **Prévia da mensagem:**
  > *"Olá João Silva! Seu pedido #1024 (Banner em lona) foi atualizado para: Pronto para retirada."*
- **Ações:**
  - Botão cinza: `[ Não enviar ]`.
  - Botão verde (WhatsApp): `[ Enviar Notificação ]`.
- **Resultado esperado:** Permitir que o operador confira os dados antes de disparar a mensagem.

### Frame 3 — Feedback do envio
- **Comportamento:** A tela exibe um aviso informando o resultado:
  - **Sucesso:** Alerta verde — *"Pedido salvo e notificação de WhatsApp enviada com sucesso para (11) 99999-9999!"*.
  - **Falha:** Alerta em caso de erro na comunicação com o serviço externo.

### Frame 4 — Histórico de notificações
- **Título:** "Histórico de Notificações WhatsApp".
- **Tabela:** Exibe data/hora, número do pedido, cliente, telefone e status (enviada ou falha).

---

## 3. Fluxo principal de navegação

1. O funcionário acessa o sistema e consulta o estoque.
2. Identifica o material pelo código de barras e informa a quantidade recebida.
3. O sistema valida os dados e registra a entrada no estoque.
4. Ao atualizar o status de um pedido, o funcionário visualiza o modal do WhatsApp e decide se envia a notificação.
5. O sistema informa se a mensagem foi enviada e grava no histórico para o administrador consultar.