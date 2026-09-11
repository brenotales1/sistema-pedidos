# Plano de Testes — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

**Equipe:** Breno Tales de Oliveira Leite (RA: 2840482423029) — Daniel Fredi Soares Pereira (RA: 2840482421054) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

---

## 1. Estratégia

| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| **Unitário** | Regras de negócio isoladas (validações de cadastro, cálculo de dimensões e restrições de estoque) | Python `unittest` | A cada PR (CI) |
| **Integração** | Rotas da API e controladores Flask (autenticação de perfis, cadastro e identificação de material) contra banco de teste | Flask Test Client + `unittest` | A cada PR (CI), a partir da Sprint 2 |
| **Manual / Aceitação** | Fluxos completos de ponta a ponta antes de cada entrega | Roteiro manual | Ao fim de cada sprint |

---

## 2. Critério de bloqueio de merge

Nenhum PR é aceito na `main` ou `develop` se: (a) algum teste automatizado existente quebrar; (b) uma nova regra de negócio (ex.: validação de código de barras único) for adicionada sem teste unitário correspondente; (c) não houver revisão e aprovação de ao menos 1 outro integrante da equipe.

---

## 3. Casos de teste planejados (cresce a cada sprint)

| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|:---:|:---:|---|---|---|:---:|
| **CT01** | #1 | Login com credenciais inválidas | `email = "admin@empresa.com.br"`, `senha = "senha_errada"` | Sistema recusa o acesso e exibe mensagem de erro | **Alta** |
| **CT02** | #1 | Acesso restrito de acordo com o perfil | Usuário com perfil `Funcionário` tentando acessar rota exclusiva de administrador | Sistema bloqueia o acesso e exibe mensagem de permissão negada | **Alta** |
| **CT03** | #2 | Cadastro de material com código de barras duplicado | `codigo_barras = "7890000000011"` (já cadastrado no banco) | Sistema recusa o cadastro (constraint de unicidade) e informa erro | **Alta** |
| **CT04** | #3 | Consulta por material inexistente no estoque | Busca por código ou nome não cadastrado | Sistema informa que o material não foi encontrado | **Média** |
| **CT05** | #5 | Entrada de estoque com quantidade inválida (menor ou igual a zero) | `quantidade = 0` ou `quantidade = -5.0` | Sistema recusa a movimentação e exige quantidade positiva | **Alta** |

*(A partir da E5, cada linha nova aqui precisa de uma evidência de execução correspondente — ver `E5-E8_evidencias_de_teste.md`.)*
