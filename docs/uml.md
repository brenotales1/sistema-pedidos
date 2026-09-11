# Diagramas UML — Sistema Web de Controle de Estoque para Empresa de Comunicação Visual

## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
  Admin((Administrador))
  Func((Funcionario))

  Admin --> UC1[Acessar o sistema com usuario e senha]
  Admin --> UC2[Cadastrar material com codigo de barras]
  Admin --> UC3[Consultar materiais cadastrados]
  Admin --> UC10[Consultar notificacoes enviadas]
  Admin --> UC11[Visualizar materiais abaixo do estoque minimo]
  Admin --> UC12[Visualizar painel de pedidos e estoque]

  Func --> UC3
  Func --> UC4[Identificar material pelo codigo de barras]
  Func --> UC5[Registrar entrada de material pelo codigo de barras]
  Func --> UC6[Consultar movimentacoes do estoque]
  Func --> UC7[Selecionar atualizacao do pedido]
  Func --> UC8[Enviar notificacao pelo WhatsApp]
  Func --> UC9[Enviar notificacao automatica por evento do pedido]

  UC5 -.include.-> UC4
  UC9 -.include.-> UC8
```

## 2. Diagrama de Classes

```mermaid
classDiagram
  direction LR

  class Perfil {
    +id: int
    +nome: string
    +descricao: string
  }

  class Usuario {
    +id: int
    +nome: string
    +email: string
    +senhaHash: string
  }

  class Administrador {
    +gerenciarUsuarios()
    +consultarNotificacoes()
    +visualizarDashboard()
  }

  class Funcionario {
    +consultarPedidos()
    +registrarEntradaEstoque()
    +atualizarPedido()
  }

  class MovimentacaoEstoque {
    +id: int
    +tipo: enum
    +quantidade: float
    +data: datetime
  }

  class Material {
    +id: int
    +nome: string
    +categoria: string
    +codigoBarras: string
    +larguraM: float
    +estoqueMinimo: float
    +metrosDisponiveis()
  }

  class BobinaEstoque {
    +id: int
    +metrosRestantes: float
  }

  class ConsumoMaterial {
    +id: int
    +metrosConsumidos: float
    +larguraBobinaUsadaM: float
    +orientacao: string
  }

  class Pedido {
    +id: int
    +status: string
    +quantidade: int
    +areaTotalM2: float
    +criadoEm: datetime
  }

  class ItemPedido {
    +id: int
    +larguraPedidoM: float
    +alturaPedidoM: float
    +quantidade: int
    +areaTotalM2: float
  }

  class ProdutoServico {
    +id: int
    +nome: string
    +descricao: string
    +valor: float
  }

  class Cliente {
    +id: int
    +nome: string
    +telefone: string
    +empresa: string
  }

  class NotificacaoWhatsApp {
    +id: int
    +mensagem: string
    +dataEnvio: datetime
    +status: enum
  }

  Usuario "N" -- "1" Perfil : possui
  Administrador --|> Usuario
  Funcionario --|> Usuario

  Usuario "1" -- "N" MovimentacaoEstoque : registra
  Material "1" -- "N" MovimentacaoEstoque : movimenta
  Material "1" -- "N" BobinaEstoque : possui

  Material "1" -- "N" ConsumoMaterial : utilizado_em
  Pedido "1" -- "N" ConsumoMaterial : consome

  Pedido "1" -- "N" ItemPedido : contem
  ProdutoServico "1" -- "N" ItemPedido : compoe

  Cliente "1" -- "N" Pedido : realiza
  Pedido "1" -- "N" NotificacaoWhatsApp : gera
  Cliente "1" -- "N" NotificacaoWhatsApp : recebe
```

## 3. Rastreabilidade — caso de uso - história do backlog

| Caso de uso | História(s) relacionada(s) (E2) |
|---|---|
| Acessar o sistema com usuario e senha | #1 |
| Cadastrar material com codigo de barras | #2 |
| Consultar materiais cadastrados | #3 |
| Identificar material pelo codigo de barras | #4 |
| Registrar entrada de material pelo codigo de barras | #5 |
| Consultar movimentacoes do estoque | #6 |
| Selecionar atualizacao do pedido | #7 |
| Enviar notificacao pelo WhatsApp | #8 |
| Enviar notificacao automatica por evento do pedido | #9 |
| Consultar notificacoes enviadas | #10 |
| Visualizar materiais abaixo do estoque minimo | #11 |
| Visualizar painel de pedidos e estoque | #12 |