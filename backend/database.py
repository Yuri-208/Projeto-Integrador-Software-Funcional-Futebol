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

    def seed_amostras():
        cursor.execute(
            "INSERT INTO clubes (nome, pais, ano_fundacao, titulos) VALUES (?, ?, ?, ?)",
            ("Grêmio", "Brasil", 1903, 60),
        )
        gremio_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO clubes (nome, pais, ano_fundacao, titulos) VALUES (?, ?, ?, ?)",
            ("Barcelona", "Espanha", 1899, 97),
        )
        barcelona_id = cursor.lastrowid

        jogadores = [
            ("Brenno", 28, "Goleiro", gremio_id),
            ("Rafinha", 40, "Lateral Direito", gremio_id),
            ("Geromel", 39, "Zagueiro", gremio_id),
            ("Victor Cuesta", 34, "Zagueiro", gremio_id),
            ("Vanderson", 23, "Lateral Esquerdo", gremio_id),
            ("Richard Ríos", 24, "Volante", gremio_id),
            ("Campaz", 22, "Meia", gremio_id),
            ("Lucas Leiva", 36, "Volante", gremio_id),
            ("Elias Manoel", 24, "Atacante", gremio_id),
            ("Diego Souza", 39, "Atacante", gremio_id),
            ("Patrick", 31, "Meia", gremio_id),
            ("Ter Stegen", 31, "Goleiro", barcelona_id),
            ("Sergi Roberto", 33, "Lateral Direito", barcelona_id),
            ("Jules Koundé", 26, "Zagueiro", barcelona_id),
            ("Frenkie de Jong", 26, "Volante", barcelona_id),
            ("Pedri", 21, "Meia", barcelona_id),
            ("Lamine Yamal", 16, "Ala", barcelona_id),
            ("João Félix", 24, "Atacante", barcelona_id),
            ("Robert Lewandowski", 36, "Atacante", barcelona_id),
            ("Ferran Torres", 24, "Atacante", barcelona_id),
            ("Alejandro Balde", 20, "Lateral Esquerdo", barcelona_id),
            ("Gündoğan", 34, "Meia", barcelona_id),
        ]

        cursor.executemany(
            "INSERT INTO jogadores (nome, idade, posicao, clube_id) VALUES (?, ?, ?, ?)",
            jogadores,
        )
        conn.commit()

        cursor.execute("SELECT id, nome FROM jogadores ORDER BY id")
        jogador_ids = {nome: jogador_id for jogador_id, nome in cursor.fetchall()}

        estatisticas_por_nome = [
            ("Brenno", 34, 0, 0, 3060, 2, 0),
            ("Rafinha", 32, 1, 4, 2800, 3, 0),
            ("Geromel", 30, 2, 1, 2700, 4, 0),
            ("Victor Cuesta", 31, 3, 0, 2750, 5, 0),
            ("Vanderson", 33, 2, 8, 2890, 2, 0),
            ("Richard Ríos", 28, 1, 5, 2650, 7, 0),
            ("Campaz", 35, 6, 10, 3000, 3, 0),
            ("Lucas Leiva", 29, 2, 6, 2920, 6, 0),
            ("Elias Manoel", 31, 12, 5, 2650, 2, 0),
            ("Diego Souza", 30, 10, 7, 2550, 5, 0),
            ("Patrick", 33, 7, 8, 2930, 4, 0),
            ("Ter Stegen", 34, 0, 0, 3060, 1, 0),
            ("Sergi Roberto", 32, 1, 5, 2800, 3, 0),
            ("Jules Koundé", 33, 2, 3, 2740, 4, 0),
            ("Frenkie de Jong", 34, 8, 9, 2900, 1, 0),
            ("Pedri", 30, 6, 12, 2980, 1, 0),
            ("Lamine Yamal", 31, 15, 18, 2840, 2, 0),
            ("João Félix", 32, 10, 7, 2770, 3, 0),
            ("Robert Lewandowski", 30, 22, 6, 2950, 2, 0),
            ("Ferran Torres", 28, 11, 9, 2860, 4, 0),
            ("Alejandro Balde", 25, 9, 10, 2920, 2, 0),
            ("Gündoğan", 27, 5, 7, 2870, 1, 0),
        ]

        estatisticas = [
            (
                jogador_ids[nome], jogos, gols, assistencias, minutos, amarelos, vermelhos
            )
            for nome, jogos, gols, assistencias, minutos, amarelos, vermelhos in estatisticas_por_nome
        ]
        cursor.executemany(
            "INSERT INTO estatisticas (jogador_id, jogos, gols, assistencias, minutos_jogados, cartoes_amarelos, cartoes_vermelhos) VALUES (?, ?, ?, ?, ?, ?, ?)",
            estatisticas,
        )

        valores_por_nome = [
            ("Brenno", 4.0, "2026-05-27"),
            ("Rafinha", 2.5, "2026-05-27"),
            ("Geromel", 2.0, "2026-05-27"),
            ("Victor Cuesta", 1.8, "2026-05-27"),
            ("Vanderson", 3.0, "2026-05-27"),
            ("Richard Ríos", 2.2, "2026-05-27"),
            ("Campaz", 4.5, "2026-05-27"),
            ("Lucas Leiva", 1.5, "2026-05-27"),
            ("Elias Manoel", 6.0, "2026-05-27"),
            ("Diego Souza", 5.0, "2026-05-27"),
            ("Patrick", 3.5, "2026-05-27"),
            ("Ter Stegen", 18.0, "2026-05-27"),
            ("Sergi Roberto", 6.0, "2026-05-27"),
            ("Jules Koundé", 9.5, "2026-05-27"),
            ("Frenkie de Jong", 40.0, "2026-05-27"),
            ("Pedri", 30.0, "2026-05-27"),
            ("Lamine Yamal", 28.0, "2026-05-27"),
            ("João Félix", 45.0, "2026-05-27"),
            ("Robert Lewandowski", 35.0, "2026-05-27"),
            ("Ferran Torres", 22.0, "2026-05-27"),
            ("Alejandro Balde", 50.0, "2026-05-27"),
            ("Gündoğan", 25.0, "2026-05-27"),
        ]

        valores = [
            (jogador_ids[nome], valor, data)
            for nome, valor, data in valores_por_nome
        ]
        cursor.executemany(
            "INSERT INTO valores_mercado (jogador_id, valor, data_atualizacao) VALUES (?, ?, ?)",
            valores,
        )
        conn.commit()

    if not has_clubes:
        seed_amostras()
    elif has_clubes and has_jogadores and has_estatisticas and has_valores:
        cursor.execute('SELECT COUNT(*) FROM jogadores')
        jogador_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM estatisticas')
        estatistica_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM valores_mercado')
        valor_count = cursor.fetchone()[0]
        if jogador_count == 2 and estatistica_count == 2 and valor_count == 2:
            cursor.execute('SELECT nome FROM jogadores ORDER BY id')
            nomes = [row[0] for row in cursor.fetchall()]
            if set(nomes) == {"Raphinha", "Arthur"}:
                cursor.execute('DELETE FROM valores_mercado')
                cursor.execute('DELETE FROM estatisticas')
                cursor.execute('DELETE FROM jogadores')
                cursor.execute('DELETE FROM clubes')
                conn.commit()
                seed_amostras()

    conn.close()
    print("Banco de dados inicializado com sucesso.")
