import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "futebol.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_bd():
    """Cria o banco de dados e as tabelas se não existirem."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clubes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT,
            ano_fundacao INTEGER,
            titulos INTEGER DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            posicao TEXT,
            clube_id INTEGER,
            FOREIGN KEY (clube_id) REFERENCES clubes(id) ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS estatisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador_id INTEGER UNIQUE,
            jogos INTEGER DEFAULT 0,
            gols INTEGER DEFAULT 0,
            assistencias INTEGER DEFAULT 0,
            minutos_jogados INTEGER DEFAULT 0,
            cartoes_amarelos INTEGER DEFAULT 0,
            cartoes_vermelhos INTEGER DEFAULT 0,
            FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS valores_mercado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador_id INTEGER,
            valor REAL,
            data_atualizacao DATE,
            FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()

    cursor.execute("SELECT 1 FROM clubes LIMIT 1")
    has_clubes = cursor.fetchone() is not None
    cursor.execute("SELECT 1 FROM jogadores LIMIT 1")
    has_jogadores = cursor.fetchone() is not None
    cursor.execute("SELECT 1 FROM estatisticas LIMIT 1")
    has_estatisticas = cursor.fetchone() is not None
    cursor.execute("SELECT 1 FROM valores_mercado LIMIT 1")
    has_valores = cursor.fetchone() is not None

    if not has_clubes and not has_jogadores and not has_estatisticas and not has_valores:
        cursor.execute(
            "INSERT INTO clubes (nome, pais, ano_fundacao, titulos) VALUES (?, ?, ?, ?)",
            ("Grêmio", "Brasil", 1903, 60),
        )
        cursor.execute(
            "INSERT INTO clubes (nome, pais, ano_fundacao, titulos) VALUES (?, ?, ?, ?)",
            ("Barcelona", "Espanha", 1899, 97),
        )

        cursor.execute(
            "INSERT INTO jogadores (nome, idade, posicao, clube_id) VALUES (?, ?, ?, ?)",
            ("Raphinha", 36, "Atacante", 2),
        )
        cursor.execute(
            "INSERT INTO jogadores (nome, idade, posicao, clube_id) VALUES (?, ?, ?, ?)",
            ("Arthur", 28, "Meia", 1),
        )

        cursor.execute(
            "INSERT INTO estatisticas (jogador_id, jogos, gols, assistencias, minutos_jogados) VALUES (?, ?, ?, ?, ?)",
            (1, 30, 20, 10, 2500),
        )
        cursor.execute(
            "INSERT INTO estatisticas (jogador_id, jogos, gols, assistencias, minutos_jogados) VALUES (?, ?, ?, ?, ?)",
            (2, 25, 8, 12, 2100),
        )

        cursor.execute(
            "INSERT INTO valores_mercado (jogador_id, valor, data_atualizacao) VALUES (?, ?, ?)",
            (1, 5.5, "2026-01-01"),
        )
        cursor.execute(
            "INSERT INTO valores_mercado (jogador_id, valor, data_atualizacao) VALUES (?, ?, ?)",
            (2, 3.0, "2026-01-01"),
        )
        conn.commit()

    conn.close()
    print("Banco de dados inicializado com sucesso.")
