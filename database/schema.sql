-- DDL SQLite do modelo implementado; E3 historica em docs/E3-schema.sql.

-- Atualizacao N:N: 15/11/2026. Nao executa migracao de dados.

PRAGMA foreign_keys = ON;

CREATE TABLE categoria_material (
	id INTEGER NOT NULL,
	nome VARCHAR(50) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (nome)
);

CREATE TABLE cliente (
	id INTEGER NOT NULL,
	nome VARCHAR(120) NOT NULL,
	telefone VARCHAR(20),
	empresa VARCHAR(120),
	PRIMARY KEY (id)
);

CREATE TABLE material (
	id INTEGER NOT NULL,
	categoria VARCHAR(50) NOT NULL,
	nome VARCHAR(120) NOT NULL,
	largura_m FLOAT NOT NULL,
	codigo_barras VARCHAR(50) NOT NULL,
	estoque_minimo FLOAT DEFAULT '0' NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT uq_material_variacao UNIQUE (categoria, nome, largura_m),
	UNIQUE (codigo_barras)
);

CREATE TABLE usuario (
	id INTEGER NOT NULL,
	nome VARCHAR(100) NOT NULL,
	email VARCHAR(120) NOT NULL,
	senha_hash VARCHAR(255) NOT NULL,
	perfil VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (email)
);

CREATE TABLE bobina_estoque (
	id INTEGER NOT NULL,
	material_id INTEGER NOT NULL,
	metros_restantes FLOAT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(material_id) REFERENCES material (id)
);

CREATE TABLE movimentacao_estoque (
	id INTEGER NOT NULL,
	material_id INTEGER NOT NULL,
	tipo VARCHAR(20) NOT NULL,
	quantidade_metros FLOAT NOT NULL,
	quantidade_bobinas INTEGER NOT NULL,
	motivo VARCHAR(255),
	usuario_id INTEGER,
	data_hora DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(material_id) REFERENCES material (id),
	FOREIGN KEY(usuario_id) REFERENCES usuario (id)
);

CREATE TABLE pedido (
	id INTEGER NOT NULL,
	cliente_id INTEGER,
	cliente_nome VARCHAR(120) NOT NULL,
	categoria VARCHAR(50) NOT NULL,
	material_nome VARCHAR(120) NOT NULL,
	largura_pedido_m FLOAT NOT NULL,
	altura_pedido_m FLOAT NOT NULL,
	quantidade INTEGER NOT NULL,
	unidade_medida VARCHAR(10) NOT NULL,
	largura_bobina_usada_m FLOAT NOT NULL,
	orientacao VARCHAR(30) NOT NULL,
	metros_consumidos FLOAT NOT NULL,
	area_total_m2 FLOAT NOT NULL,
	status VARCHAR(30) NOT NULL,
	criado_em DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(cliente_id) REFERENCES cliente (id)
);

CREATE TABLE consumo_material (
	pedido_id INTEGER NOT NULL,
	material_id INTEGER NOT NULL,
	quantidade_metros FLOAT NOT NULL,
	principal BOOLEAN NOT NULL,
	PRIMARY KEY (pedido_id, material_id),
	CONSTRAINT ck_consumo_material_positivo CHECK (quantidade_metros > 0),
	FOREIGN KEY(pedido_id) REFERENCES pedido (id),
	FOREIGN KEY(material_id) REFERENCES material (id)
);

CREATE TABLE historico_status_pedido (
	id INTEGER NOT NULL,
	pedido_id INTEGER NOT NULL,
	status_anterior VARCHAR(30) NOT NULL,
	novo_status VARCHAR(30) NOT NULL,
	usuario_id INTEGER NOT NULL,
	data_hora DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(pedido_id) REFERENCES pedido (id),
	FOREIGN KEY(usuario_id) REFERENCES usuario (id)
);

CREATE TABLE notificacao_whatsapp (
	id INTEGER NOT NULL,
	historico_status_id INTEGER NOT NULL,
	pedido_id INTEGER NOT NULL,
	cliente_id INTEGER NOT NULL,
	data_hora DATETIME NOT NULL,
	evento VARCHAR(40) NOT NULL,
	resultado VARCHAR(30) NOT NULL,
	message_sid VARCHAR(34),
	codigo_erro INTEGER,
	entrega_confirmada BOOLEAN NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (historico_status_id),
	FOREIGN KEY(historico_status_id) REFERENCES historico_status_pedido (id),
	FOREIGN KEY(pedido_id) REFERENCES pedido (id),
	FOREIGN KEY(cliente_id) REFERENCES cliente (id)
);
