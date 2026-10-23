# Ata de Retrospectiva — Sprint 3 — Sistema de Pedidos e Controle de Estoque

**Data:** 18/10/2026 (consolidação técnica — Entrega E7)  
**Presentes:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
|---|:---:|---|
| Implementar seleção de atualização de status do pedido para disparo de avisos (US #7) | Sim | Atualização de status com cliente associado e histórico de transição implementada por Breno. |
| Implementar envio de notificação via WhatsApp para clientes (US #8) | Sim | Conector com a Meta Cloud API via `requests`, com registro persistido de cada tentativa de envio. O aceite da API não confirma a entrega ao cliente. |
| Implementar disparos automáticos de mensagens em eventos de mudança de status (US #9) | Sim | Evento de finalização integrado ao envio automático. Falhas da API ou de rede preservam a finalização do pedido. |
| Desenvolver casos de teste automatizados para o módulo de notificações (CT08 e CT09) | Sim | 21 novos testes de notificação e 68 testes aprovados no total. Como CT08 e CT09 já identificavam cenários de autenticação, os cenários de notificação foram formalizados em CT42–CT45, com equivalência documentada. |

---

## 2. O que funcionou bem

- **Divisão de responsabilidades:** A implementação de Breno e a validação/documentação de Daniel permitiram exercitar o conector existente sem alterar seu comportamento.
- **Persistência do Pedido:** A finalização é persistida antes da chamada externa, garantindo que falhas da Meta ou de rede não desfaçam o pedido.
- **Testes Reproduzíveis:** O SQLite em memória e os mocks permitiram validar os cenários sem credenciais de produção, com 68 testes aprovados no total.
- **Rastreabilidade das Notificações:** O histórico permite relacionar cada tentativa ao cliente, ao pedido e ao usuário responsável pela transição.

---

## 3. O que não funcionou

- **Confirmação de Entrega:** O aceite HTTP da Meta não comprova a entrega ao cliente. Os testes verificam `aceito` e `entrega_confirmada=False`, e a documentação explicita essa limitação do webhook.
- **Simulação de Falhas e Bloqueio em Testes:** Foi necessário simular HTTP 400/500, timeout e erro de conexão com mocks de `requests.post`. Para validar o sucesso, o modo testing foi desativado localmente somente após a instalação do mock e de uma barreira adicional na sessão HTTP. Fixtures fictícias e substituição das variáveis Meta, com restauração automática, evitaram o uso de telefones e credenciais reais.
- **Ambiente Python sem Dependências:** O Python global não continha as dependências necessárias; a execução foi realizada com o ambiente `.venv` existente no projeto.
- **Conflito na Identificação dos Casos de Teste:** Os IDs CT08 e CT09 previstos na Sprint 2 já eram utilizados para autenticação. Os cenários de notificação foram registrados em CT42–CT45, preservando os IDs anteriores e documentando a equivalência.

---

## 4. Ações para a próxima sprint — Sprint 4 (Sprint Final)

A Sprint 4 será a última etapa do projeto, tendo como principal objetivo finalizar o MVP, validar as funcionalidades implementadas e preparar o sistema para a entrega final.

| Ação | Responsável |
|---|---|
| Implementar consulta administrativa do histórico de notificações (US #10 / CT46), conforme prioridade do backlog. | Breno Tales e Daniel Fredi |
| Revisar a integração com a Meta Cloud API, corrigindo possíveis falhas no envio e no registro das notificações. | Breno Tales|
| Validar a identificação de materiais e a entrada de estoque por código de barras, utilizando inicialmente a digitação manual e, caso disponível, um leitor físico USB HID. | Daniel Fredi |
| Corrigir possíveis erros e realizar os ajustes finais nas funcionalidades de pedidos, clientes e estoque. | Breno Tales e Daniel Fredi|
| Executar os testes automatizados e registrar as evidências de funcionamento do sistema. | Daniel Fredi|
| Revisar os requisitos obrigatórios (Must Have) e verificar o atendimento aos critérios de aceite do MVP. | Breno Tales e Daniel Fredi |
| Atualizar a documentação técnica, os relatórios e as evidências da Sprint 4. | Daniel Fredi |
| Preparar a apresentação e a demonstração do sistema para a avaliação final. | Breno Tales e Daniel Fredi  |

