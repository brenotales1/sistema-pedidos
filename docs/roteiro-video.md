# Roteiro de Apresentação e Vídeo — Center Pedidos

> **Observação de rastreabilidade:** Este arquivo atende diretamente ao requisito de entrega de roteiro do vídeo e da apresentação do projeto Center Pedidos (equivalente ao `docs/roteiro-apresentacao.md` da especificação da E10).

**Projeto:** Center Pedidos — Sistema Web de Gestão de Pedidos, Estoque de Bobinas e Automação de Avisos via WhatsApp para Empresa de Comunicação Visual  
**Trilha:** A1 (TCC vinculado ao Laboratório de Engenharia de Software)  
**Equipe:**
- Breno Tales de Oliveira Leite — RA: 2840482423029
- Daniel Fredi Soares Pereira — RA: 2840482421054

**Links de Entrega:**
- **Vídeo da Mostra Virtual (YouTube):** [https://www.youtube.com/watch?v=42EjsnOwr6k](https://www.youtube.com/watch?v=42EjsnOwr6k) (Duração: 10:00)
- **Deploy em Produção:** [https://center-pedidos.onrender.com](https://center-pedidos.onrender.com)
- **Repositório GitHub:** [https://github.com/brenotales1/sistema-pedidos](https://github.com/brenotales1/sistema-pedidos)

---

## 1. Vídeo de Demonstração e Mostra Virtual (Gravação de Tela + Narração)

| Tempo | Conteúdo | Quem narra |
|---|---|---|
| **00:00 – 01:34** | **Abertura, Contexto do Cliente e Gargalos Operacionais:** Apresentação da equipe e da empresa familiar de comunicação visual parceira (~40 pedidos semanais, estoque de bobinas de lona, adesivos vinílicos e tecidos). Demonstração das dores reais pré-sistema: falta de centralização dos pedidos, conferência manual de estoque (~1h/semana) e notificações manuais aos clientes via WhatsApp (~4h semanais de trabalho repetitivo sujeito a esquecimentos). Delimitação entre a base do TCC (aproveitamento de corte) e os incrementos do Laboratório (integração Meta WhatsApp Cloud API, leitor de código de barras, estoque mínimo e suíte de testes). | **Daniel e Breno** |
| **01:34 – 02:33** | **Controle de Acesso por Perfis (RBAC):** Demonstração ao vivo no Render. Login com perfil *Funcionário* evidenciando a restrição de rotas administrativas e menus adaptados à rotina operacional. Login com perfil *Administrador* desbloqueando o painel de auditoria, histórico de notificações e parametrizações globais do sistema. | **Daniel Fredi** |
| **02:33 – 03:51** | **Gestão de Estoque e Entrada por Código de Barras:** Demonstração do saldo consolidado em metros por categoria de material. Visualização dos badges de alerta de estoque mínimo e filtragem para reposição rápida. Teste de validação defensiva com códigos inválidos e duplicados. Leitura real de código de barras de bobina de lona brilho com entrada de 2 bobinas de 50 m (+100 m adicionados ao saldo) e registro atômico no histórico de movimentações com rastreabilidade completa (data, hora, material, quantidade, tipo, usuário e justificativa). | **Breno Leite** |
| **03:51 – 04:35** | **Fluxo Principal de Pedidos e Relação N:N (`ConsumoMaterial`):** Cadastro de novo pedido com cliente cadastrado. Aplicação do algoritmo de cálculo de aproveitamento de corte para redução de aparas de bobinas. Explicação da modelagem da entidade associativa `ConsumoMaterial`, permitindo relação N:N estrita com controle individual de baixa de múltiplos insumos por pedido e rastreio de consumo por material. | **Breno Leite** |
| **04:35 – 06:17** | **Automação do WhatsApp e Resiliência Transacional:** Atualização do status do pedido para "Pronto para Retirada". Disparo automático da mensagem transacional personalizada via Meta WhatsApp Cloud API. Demonstração de tolerância a falhas: desacoplamento entre a persistência do pedido e a chamada HTTP externa. Se o serviço de mensageria oscilar, o status do pedido permanece íntegro no banco e o incidente é gravado no log de auditoria sem travar a produção. | **Breno e Daniel** |
| **06:17 – 07:23** | **Engenharia Ágil e Evolução da Cobertura de Testes:** Detalhamento da evolução das 4 sprints quinzenais: S1 (24 testes — autenticação e base), S2 (41 testes — código de barras e movimentações), S3 (68 testes — integração Meta WhatsApp API), S4 (115 testes — estoque mínimo e histórico) e consolidação final na E10 com **131 testes unitários** automatizados aprovados (incluindo cobertura de `ConsumoMaterial`). | **Daniel e Breno** |
| **07:23 – 08:01** | **Retrospectivas Práticas e Gestão de Escopo:** Lições das retrospectivas ágeis da equipe. Resolução do problema de concorrência e locks no banco de dados durante testes da Sprint 2 com o isolamento de instâncias de teste. Decisão consciente de adiar gráficos visuais para assegurar 100% de robustez no motor de mensageria e na integridade do estoque. | **Breno Leite** |
| **08:01 – 08:44** | **Revezamento de Papéis e Aprendizado Técnico (Breno):** Revezamento entre desenvolvimento e qualidade de software. Foco em QA na S1 e S4, leitor de código de barras na S2 e integração da API da Meta na S3. Aprendizado prático: a suíte de testes deixou de ser vista como custo e provou ser o pilar indispensável para refatorar regras críticas de negócio sem regressões. | **Breno Leite** |
| **08:44 – 09:39** | **Revezamento de Papéis e Aprendizado Técnico (Daniel):** Atuação em autenticação na S1, relatório de movimentações na S2, testes e mocks de API na S3, e histórico de notificações e estoque mínimo na S4. Aprendizado prático: a importância de projetar software para lidar com cenários reais de exceção e falha de serviços externos em ambientes de missão crítica. | **Daniel Fredi** |
| **09:39 – 10:00** | **Fechamento e Disponibilização dos Artefatos:** Divulgação dos links de produção no Render, repositório GitHub com documentação rastreada de E1 a E10, manuais de usuário e agradecimentos ao orientador Prof. Lucas e à banca avaliadora. | **Breno Leite** |

---

## 2. Pitch ao Vivo (10 min de Apresentação + 5 min de Perguntas da Banca)

| Bloco | Tempo | Quem fala | Conteúdo |
|---|---|---|---|
| **1. Contexto, Problema e Cliente Real** | 2 min | **Daniel Fredi** | Apresentação da empresa de comunicação visual parceira (4 funcionários, ~40 pedidos semanais). Apresentação dos dois grandes gargalos: 1h/semana de medição física manual de rolos e 4h/semana de digitação de avisos no WhatsApp. Proposta de valor: eliminar retrabalho e perdas por meio de software web integrado. |
| **2. Demonstração Operacional em Produção** | 3 min | **Daniel Fredi** | Demonstração ao vivo no ambiente do Render: autenticação por perfil (Admin vs. Funcionário), entrada rápida de bobinas por código de barras com baixa e soma atômica, consulta com alerta de estoque mínimo e criação de pedido com consumo N:N de materiais. |
| **3. Arquitetura, Integrações e Resiliência** | 2 min | **Breno Leite** | Demonstração do ciclo de vida de status do pedido e acionamento da Meta WhatsApp Cloud API. Explicação da arquitetura em camadas (`controllers/`, `services/`, `models/`), persistência desacoplada da rede, tratamento de falhas e auditoria de status e mensagens. |
| **4. Engenharia de Qualidade e Processo Ágil** | 2 min | **Breno Leite** | Apresentação da suíte de 131 testes automatizados cobrindo histórias de usuário ponta a ponta. Demonstração de como os testes viabilizaram a migração segura da modelagem N:N e o isolamento do banco. Análise das retrospectivas das Sprints 1 a 4. |
| **5. Fechamento e Próximos Passos** | 1 min | **Daniel + Breno** | Síntese dos resultados obtidos no MVP, validação com o cliente real, termo de aceite e visão de evolução futura (painéis de gráficos gerenciais e integração contínua). |

---

## 3. Perguntas Antecipadas da Banca e Respostas Preparadas

| Pergunta Provável da Banca | Quem responde | Resposta Preparada |
|---|---|---|
| **Como vocês garantem que a falha da API do WhatsApp ou uma queda de conexão não invalida o pedido do cliente?** | **Daniel Fredi** | *No `whatsapp_service.py`, a chamada externa HTTP é desacoplada da transação do banco de dados. A transação que atualiza o status do pedido no SQLAlchemy é confirmada primeiro (`commit`). O envio da notificação ocorre em seguida, com captura de qualquer exceção HTTP ou erro da Meta. Em caso de falha, o status do pedido permanece intacto e gravamos uma ocorrência no histórico de notificações indicando o erro para retentativa posterior.* |
| **Por que a relação entre Pedido e Material foi modelada com a entidade associativa `ConsumoMaterial`?** | **Breno Leite** | *Porque um pedido de comunicação visual consome diferentes tipos de materiais em proporções distintas (ex.: 12 m de lona brilho e 20 unidades de ilhós), e o mesmo lote de material atende diversos pedidos fracionados ao longo da semana. A entidade `ConsumoMaterial` resolve o relacionamento N:N e armazena atributos específicos da associação, como a metragem consumida e a data de baixa.* |
| **Como o sistema se comporta quando múltiplos funcionários realizam movimentações de estoque simultâneas?** | **Daniel Fredi** | *As movimentações de entrada e saída são tratadas como transações atômicas no serviço de estoque. Cada inserção gera um registro imutável em `MovimentacaoEstoque` com data, hora, usuário logado e quantidade, atualizando o saldo do material correspondente dentro de uma mesma transação do banco.* |
| **Qual foi o papel da suíte de 131 testes automatizados durante a evolução do projeto?** | **Breno Leite** | *Os testes foram desenvolvidos de forma incremental em cada sprint (24 $\rightarrow$ 41 $\rightarrow$ 68 $\rightarrow$ 115 $\rightarrow$ 131). Quando precisamos refatorar a estrutura do banco na reta final para introduzir a migração do `ConsumoMaterial` N:N e o isolamento de sessões de teste, a suíte completa executou em menos de 20 segundos, garantindo regressão zero em todas as histórias de usuário anteriores.* |
| **O que a equipe faria de diferente se fosse reiniciar o semestre hoje?** | **Daniel Fredi** | *Teríamos estabelecido o fluxo rigoroso de branches e Pull Requests com revisão obrigatória de código desde o primeiro commit da Sprint 1, além de antecipar a configuração de variáveis de ambiente e deploy na nuvem nas primeiras semanas para evitar a sobrecarga de homologação concentrada no final.* |
| **Como foi conduzida a validação com a empresa de comunicação visual cliente?** | **Breno Leite** | *O sistema foi homologado em conjunto com a gestão da empresa parceira, validando o fluxo de ponta a ponta: cadastramento de materiais reais, entrada por leitor de código de barras nas bobinas do estoque físico e envio de avisos de teste no WhatsApp dos administradores para comprovar a economia de tempo das rotinas semanais.* |
