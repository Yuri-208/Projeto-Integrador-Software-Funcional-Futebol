-- Tabela de clubes
CREATE TABLE clubes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    pais TEXT,
    ano_fundacao INTEGER,
    titulos INTEGER DEFAULT 0
);

-- Tabela de jogadores
CREATE TABLE jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    posicao TEXT,
    clube_id INTEGER,
    FOREIGN KEY (clube_id) REFERENCES clubes(id) ON DELETE SET NULL
);

-- Tabela de estatísticas (1:1 com jogador)
CREATE TABLE estatisticas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER UNIQUE,
    jogos INTEGER DEFAULT 0,
    gols INTEGER DEFAULT 0,
    assistencias INTEGER DEFAULT 0,
    minutos_jogados INTEGER DEFAULT 0,
    cartoes_amarelos INTEGER DEFAULT 0,
    cartoes_vermelhos INTEGER DEFAULT 0,
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
);

-- Tabela de valor de mercado (histórico)
CREATE TABLE valores_mercado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER,
    valor REAL,
    data_atualizacao DATE,
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
);

-- Inserindo dados exemplo
INSERT INTO clubes (nome, pais, ano_fundacao, titulos)
VALUES 
('Grêmio', 'Brasil', 1903, 60),
('Barcelona', 'Espanha', 1899, 97);

INSERT INTO jogadores (nome, idade, posicao, clube_id)
VALUES 
('Raphinha', 36, 'Atacante', 2),
('Arthur', 28, 'Meia', 1);

INSERT INTO estatisticas (jogador_id, jogos, gols, assistencias, minutos_jogados)
VALUES 
(1, 30, 20, 10, 2500),
(2, 25, 8, 12, 2100);

INSERT INTO valores_mercado (jogador_id, valor, data_atualizacao)
VALUES 
(1, 5.5, '2026-01-01'),
(2, 3.0, '2026-01-01');