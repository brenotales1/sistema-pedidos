-- schema.sql — Sistema Web de Controle de Estoque para Empresa de Comunicacao Visual
-- Alunos: Breno Tales de Oliveira Leite - RA 2840482423029
-- Daniel Fredi Soares Pereira - RA 2840482421054

CREATE TABLE perfil (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(50) NOT NULL UNIQUE,
  descricao VARCHAR(160)
);

CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  perfil_id INT NOT NULL REFERENCES perfil(id),
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE administrador (
  id SERIAL PRIMARY KEY,
  usuario_id INT NOT NULL UNIQUE REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE funcionario (
  id SERIAL PRIMARY KEY,
  usuario_id INT NOT NULL UNIQUE REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE cliente (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  telefone VARCHAR(20),
  empresa VARCHAR(120)
);

CREATE TABLE pedido (
  id SERIAL PRIMARY KEY,
  cliente_id INT NOT NULL REFERENCES cliente(id),
  status VARCHAR(30) NOT NULL DEFAULT 'Pagamento pendente'
    CHECK (status IN ('Pagamento pendente', 'Aguardando producao', 'Pronto para retirada', 'Finalizado')),
  quantidade INT NOT NULL CHECK (quantidade > 0),
  area_total_m2 FLOAT NOT NULL CHECK (area_total_m2 >= 0),
  criado_em TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE produto_servico (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  descricao VARCHAR(255),
  valor FLOAT CHECK (valor >= 0)
);

CREATE TABLE item_pedido (
  id SERIAL PRIMARY KEY,
  pedido_id INT NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
  produto_servico_id INT NOT NULL REFERENCES produto_servico(id),
  largura_pedido_m FLOAT NOT NULL CHECK (largura_pedido_m > 0),
  altura_pedido_m FLOAT NOT NULL CHECK (altura_pedido_m > 0),
  quantidade INT NOT NULL CHECK (quantidade > 0),
  area_total_m2 FLOAT NOT NULL CHECK (area_total_m2 >= 0)
);

CREATE TABLE material (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  codigo_barras VARCHAR(80) NOT NULL UNIQUE,
  largura_m FLOAT NOT NULL CHECK (largura_m > 0),
  estoque_minimo FLOAT NOT NULL DEFAULT 0 CHECK (estoque_minimo >= 0),
  UNIQUE (categoria, nome, largura_m)
);

CREATE TABLE bobina_estoque (
  id SERIAL PRIMARY KEY,
  material_id INT NOT NULL REFERENCES material(id) ON DELETE CASCADE,
  metros_restantes FLOAT NOT NULL DEFAULT 50.0 CHECK (metros_restantes >= 0)
);

CREATE TABLE movimentacao_estoque (
  id SERIAL PRIMARY KEY,
  usuario_id INT NOT NULL REFERENCES usuario(id),
  material_id INT NOT NULL REFERENCES material(id),
  tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada', 'saida', 'ajuste')),
  quantidade FLOAT NOT NULL CHECK (quantidade > 0),
  data TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE consumo_material (
  id SERIAL PRIMARY KEY,
  pedido_id INT NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
  material_id INT NOT NULL REFERENCES material(id),
  metros_consumidos FLOAT NOT NULL CHECK (metros_consumidos > 0),
  largura_bobina_usada_m FLOAT NOT NULL CHECK (largura_bobina_usada_m > 0),
  orientacao VARCHAR(30) NOT NULL CHECK (orientacao IN ('Padrao', 'Rotacionado'))
);

CREATE TABLE notificacao_whatsapp (
  id SERIAL PRIMARY KEY,
  pedido_id INT NOT NULL REFERENCES pedido(id) ON DELETE CASCADE,
  cliente_id INT NOT NULL REFERENCES cliente(id),
  mensagem VARCHAR(500) NOT NULL,
  data_envio TIMESTAMP NOT NULL DEFAULT now(),
  status VARCHAR(20) NOT NULL CHECK (status IN ('enviada', 'falha'))
);

CREATE INDEX idx_pedido_status ON pedido(status);
CREATE INDEX idx_material_codigo_barras ON material(codigo_barras);
CREATE INDEX idx_notificacao_status ON notificacao_whatsapp(status);
CREATE INDEX idx_movimentacao_data ON movimentacao_estoque(data);

-- Seed de exemplo
INSERT INTO perfil (nome, descricao) VALUES
  ('Administrador', 'Responsavel pela gestao do sistema'),
  ('Funcionario', 'Usuario responsavel pela operacao do estoque e pedidos');

INSERT INTO usuario (perfil_id, nome, email, senha_hash) VALUES
  (1, 'Breno Tales', 'breno@empresa.com.br', '$2b$10$exemplo'),
  (2, 'Daniel Fredi', 'daniel@empresa.com.br', '$2b$10$exemplo');

INSERT INTO administrador (usuario_id) VALUES (1);
INSERT INTO funcionario (usuario_id) VALUES (2);

INSERT INTO cliente (nome, telefone, empresa) VALUES
  ('Joao Silva', '(11) 99999-9999', 'Loja Silva');

INSERT INTO produto_servico (nome, descricao, valor) VALUES
  ('Banner em lona', 'Impressao de banner em lona', 80.00),
  ('Adesivo personalizado', 'Impressao em adesivo branco brilho', 45.00);

INSERT INTO material (nome, categoria, codigo_barras, largura_m, estoque_minimo) VALUES
  ('Lona Branca Brilho', 'Lona', '7890000000011', 3.20, 20),
  ('Adesivo Branco Brilho', 'Adesivo', '7890000000028', 1.27, 15);

INSERT INTO bobina_estoque (material_id, metros_restantes) VALUES
  (1, 50.0),
  (2, 50.0);

INSERT INTO pedido (cliente_id, status, quantidade, area_total_m2) VALUES
  (1, 'Pagamento pendente', 2, 4.00);

INSERT INTO item_pedido (
  pedido_id,
  produto_servico_id,
  largura_pedido_m,
  altura_pedido_m,
  quantidade,
  area_total_m2
) VALUES
  (1, 1, 1.00, 2.00, 2, 4.00);

INSERT INTO consumo_material (
  pedido_id,
  material_id,
  metros_consumidos,
  largura_bobina_usada_m,
  orientacao
) VALUES
  (1, 1, 4.00, 3.20, 'Padrao');

INSERT INTO movimentacao_estoque (usuario_id, material_id, tipo, quantidade) VALUES
  (2, 1, 'saida', 4.00);

INSERT INTO notificacao_whatsapp (pedido_id, cliente_id, mensagem, status) VALUES
  (1, 1, 'Seu pedido foi registrado e esta com pagamento pendente.', 'enviada');