# Ata de Retrospectiva — Sprint 4 — Sistema de Pedidos e Controle de Estoque

**Data:** 10/11/2026 (consolidação técnica e encerramento do MVP — Entrega E8)  
**Presentes:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida na Sprint 3 | Responsável | Aplicada? | Evidência / Comentário |
|---|---|:---:|---|
| Implementar consulta administrativa do histórico de notificações (US #10 / CT46) | Daniel Fredi | Sim | Rota `/notificacoes` implementada no commit `695791c`, com paginação de 25 registros, filtros por status e validação estrita de perfil administrador. |
| Validar a identificação de materiais e a entrada de estoque por código de barras | Daniel Fredi e Breno Tales | Sim | Implementado suporte a digitação e leitor USB no commit `695791c`, complementado com testes de busca, API e entrada em `test_codigo_barras_materiais.py`. |
| Corrigir possíveis erros e realizar os ajustes finais nas funcionalidades de pedidos, clientes e estoque | Daniel Fredi | Sim | Regras de cancelamento seguro (bloqueio para pedidos prontos e finalizados), alertas de estoque mínimo estrito (US #11) e garantia de atomicidade no histórico de movimentações (US #6) no commit `652bd8f`. |
| Desenvolver e executar os testes automatizados e registrar as evidências de funcionamento do sistema | Breno Tales | Sim | 43 novos testes unitários e de integração desenvolvidos por Breno, totalizando 111 testes automatizados aprovados (100% de sucesso). Registrado em `sprint-4-evidencias-teste.md`. |
| Revisar os requisitos obrigatórios (Must Have) e verificar o atendimento aos critérios de aceite do MVP | Breno Tales e Daniel Fredi | Sim | Todos os requisitos Must e Should foram validados contra o termo de aceite e revisados em `sprint-4-revisao-mvp.md`. |
| Atualizar a documentação técnica, os relatórios e as evidências da Sprint 4 | Breno Tales | Sim | `backlog.md`, `plano-de-testes.md`, relatórios e atas consolidados na pasta `docs/`. |
| Preparar a apresentação e a demonstração do sistema para a avaliação final | Breno Tales e Daniel Fredi | Sim | Roteiro de demonstração estruturado cobrindo o fluxo completo: login, cadastro, leitor de código de barras, cálculo de corte, pedido, cancelamento e histórico WhatsApp. |

---

## 2. O que funcionou bem

- **Robustez dos Testes Automatizados:** A criação de 43 novos testes unitários e de integração elevou a suíte para 111 testes, cobrindo integralmente as regras de transação, cancelamento e permissões com zero regressões.
- **Isolamento e Segurança de Dados:** As travas de cancelamento e a política de histórico atômico impedem qualquer inconsistência entre saldo de estoque e histórico de movimentações.
- **Usabilidade do Estoque Mínimo:** A exibição com alerta condicional e o filtro `?abaixo_minimo=1` facilitam diretamente a tomada de decisão para compras e reposição de bobinas.
- **Consulta de Notificações sem Efeitos Colaterais:** A tela de histórico (CT46) foi construída de forma estritamente somente-leitura, garantindo que consultas administrativas nunca disparem envios acidentais.

---

## 3. O que não funcionou / Desafios enfrentados

- **Códigos de Barras em Materiais Antigos:** Como o sistema herdou materiais de cadastros anteriores da empresa, 7 itens não possuíam código de barras cadastrado. A funcionalidade de edição pelo admin resolveu isso no código, mas o preenchimento dos códigos físicos reais nas instalações da empresa ficou como tarefa operacional de implantação.
- **Ambiente de Testes Meta vs. Produção:** A dependência de URLs públicas HTTPS e tokens permanentes para o webhook real e templates aprovados exigiu que a homologação da Sprint continuasse focada em mocks rigorosos, deixando o handshake externo real para o momento do deploy em servidor com domínio e SSL.

---

## 4. Conclusão do MVP e Próximos Passos (Pós-Projeto)

Com o término da Sprint 4, o **Produto Mínimo Viável (MVP)** encontra-se finalizado, atendendo plenamente aos objetivos estabelecidos com o orientador e cliente da Fatec Ribeirão Preto:
1. Versionar e realizar o merge final da branch de entrega na `main`.
2. Realizar o deploy do sistema em provedor em nuvem com servidor WSGI (ex.: Gunicorn) e HTTPS ativo.
3. Cadastrar os códigos de barras das bobinas físicas da empresa diretamente na interface de produção.
4. Futuras iterações (versão 2.0): implementar a US #12 (Dashboard analítico com gráficos consolidados).
