# Roteiro do Protótipo Navegável — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual
## **Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

### **Link do protótipo:** https://www.figma.com/make/CITmJdPdYf8afoMoqX9TLM/prototipo-API?t=pnjhPEgDFrhV7bCw-20&fullscreen=1
---
| Tela / Componente | Perfil | História relacionada (E2) | O que a tela mostra / permite |
|---|---|:---:|---|
| **1. Identificação e Entrada por Código de Barras** | Funcionário | #4, #5 | Campo para bipar o código de barras, identificação instantânea do material e confirmação da entrada de bobinas no estoque |
| **2. Pop-up de Notificação WhatsApp (Modal)** | Funcionário | #7, #8, #9 | Pop-up exibido após salvar/atualizar o pedido, mostrando os dados do cliente e a mensagem pré-formatada com opção de confirmar ou cancelar o disparo via WhatsApp |
| **3. Feedback de Status do Envio (Toast/Alerta)** | Funcionário | #8, #9 | Notificação visual em tela informando o resultado imediato do envio da API (sucesso com mensagem enviada ou aviso de falha) |
| **4. Histórico de Notificações Enviadas** | Administrador | #10 | Tabela de auditoria exibindo todos os disparos da API: nome do cliente, pedido, telefone, data/hora e status (*enviada* ou *falha*) |
2. 
Frame 1: Entrada por Código de Barras (API Código de Barras)
Cabeçalho: "Entrada de Material no Estoque"
Campo de Input: [ Bipar ou digitar código de barras... ] com ícone de leitor.
Card de Retorno: Quando o código é lido, exibe:
Material: Lona Branca Brilho 3.20m
Categoria: Lona | Código: 7890000000011
Estoque atual: 50.0m
Campo de Quantidade: [ 50.0 ] metros
Botão principal: [ Confirmar Entrada ]

Frame 2: Tela do Pedido com o Pop-up (Modal) de WhatsApp
Fundo: A tela do pedido que já existe no sistema (levemente escurecida com transparência).
Caixa Central (Pop-up):
Título: Deseja enviar notificação ao cliente via WhatsApp?
Dados do Cliente: João Silva — (11) 99999-9999
Prévia da Mensagem:
"Olá João Silva! Seu pedido #1024 (Banner em lona) foi atualizado para: Pronto para retirada."
Botões:
Botão cinza/secundário: [ Não enviar ]
Botão verde/WhatsApp: [ Enviar Notificação ]

Frame 3: Feedback de Envio (Toast de Sucesso)
A tela do pedido retorna ao normal com um alerta verde no topo:
 Pedido salvo e notificação de WhatsApp enviada com sucesso para (11) 99999-9999!

Frame 4: Tabela de Histórico de Notificações
Título: "Histórico de Notificações WhatsApp"
Tabela simples:
Data/Hora	Pedido	Cliente	Telefone	Status
11/09 14:30	#1024	João Silva	(11) 99999-9999	🟢 Enviada
11/09 10:15	#1023	Loja ABC	(11) 98888-8888	🔴 Falha