from datetime import datetime

from .database import conectar


# CRUD CLUBES

def criar_clube(nome, pais, ano, titulos):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clubes (nome, pais, ano_fundacao, titulos) VALUES (?, ?, ?, ?)",
            (nome, pais, ano, titulos),
        )
        conn.commit()
        conn.close()
        print(f"OK: Clube '{nome}' criado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao criar clube: {e}")


def listar_clubes():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clubes")
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro: Erro ao listar clubes: {e}")
        return []


def atualizar_clube(id, nome, pais, ano, titulos):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clubes SET nome=?, pais=?, ano_fundacao=?, titulos=? WHERE id=?",
            (nome, pais, ano, titulos, id),
        )
        conn.commit()
        conn.close()
        print(f"OK: Clube ID {id} atualizado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao atualizar clube: {e}")


def deletar_clube(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clubes WHERE id=?", (id,))
        conn.commit()
        conn.close()
        print(f"OK: Clube ID {id} deletado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao deletar clube: {e}")


# CRUD JOGADORES


def criar_jogador(nome, idade, posicao, clube_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jogadores (nome, idade, posicao, clube_id) VALUES (?, ?, ?, ?)",
            (nome, idade, posicao, clube_id),
        )
        jogador_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO estatisticas (jogador_id) VALUES (?)",
            (jogador_id,),
        )

        conn.commit()
        conn.close()
        print(f"OK: Jogador '{nome}' criado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao criar jogador: {e}")


def listar_jogadores():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT j.id, j.nome, j.idade, j.posicao, c.nome
            FROM jogadores j
            LEFT JOIN clubes c ON j.clube_id = c.id
            """
        )
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro: Erro ao listar jogadores: {e}")
        return []


def atualizar_jogador(id, nome, idade, posicao, clube_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE jogadores SET nome=?, idade=?, posicao=?, clube_id=? WHERE id=?",
            (nome, idade, posicao, clube_id, id),
        )
        conn.commit()
        conn.close()
        print(f"OK: Jogador ID {id} atualizado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao atualizar jogador: {e}")


def deletar_jogador(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jogadores WHERE id=?", (id,))
        conn.commit()
        conn.close()
        print(f"OK: Jogador ID {id} deletado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao deletar jogador: {e}")


# CRUD ESTATÍSTICAS


def criar_estatistica(jogador_id, jogos, gols, assistencias, minutos, amarelos, vermelhos):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO estatisticas (jogador_id, jogos, gols, assistencias, minutos_jogados,
               cartoes_amarelos, cartoes_vermelhos) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (jogador_id, jogos, gols, assistencias, minutos, amarelos, vermelhos),
        )
        conn.commit()
        conn.close()
        print("OK: Estatística criada com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao criar estatística: {e}")


def listar_estatisticas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.id, j.nome, e.jogos, e.gols, e.assistencias,
                   e.minutos_jogados, e.cartoes_amarelos, e.cartoes_vermelhos
            FROM estatisticas e
            JOIN jogadores j ON e.jogador_id = j.id
            """
        )
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro: Erro ao listar estatísticas: {e}")
        return []


def atualizar_estatistica(jogador_id, jogos, gols, assistencias, minutos, amarelos, vermelhos):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE estatisticas SET jogos=?, gols=?, assistencias=?, minutos_jogados=?,
               cartoes_amarelos=?, cartoes_vermelhos=? WHERE jogador_id=?""",
            (jogos, gols, assistencias, minutos, amarelos, vermelhos, jogador_id),
        )
        conn.commit()
        conn.close()
        print(f"OK: Estatística do jogador ID {jogador_id} atualizada com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao atualizar estatística: {e}")


def deletar_estatistica(jogador_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM estatisticas WHERE jogador_id=?", (jogador_id,))
        conn.commit()
        conn.close()
        print("OK: Estatística deletada com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao deletar estatística: {e}")


# CRUD VALORES DE MERCADO


def criar_valor_mercado(jogador_id, valor, data=None):
    try:
        if not data:
            data = datetime.now().strftime("%Y-%m-%d")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO valores_mercado (jogador_id, valor, data_atualizacao) VALUES (?, ?, ?)",
            (jogador_id, valor, data),
        )
        conn.commit()
        conn.close()
        print("Valor de mercado registrado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar valor de mercado: {e}")


def listar_valores_mercado():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT v.id, j.nome, v.valor, v.data_atualizacao
            FROM valores_mercado v
            JOIN jogadores j ON v.jogador_id = j.id
            ORDER BY v.data_atualizacao DESC
            """
        )
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro: Erro ao listar valores de mercado: {e}")
        return []


def atualizar_valor_mercado(id, valor, data=None):
    try:
        if not data:
            data = datetime.now().strftime("%Y-%m-%d")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE valores_mercado SET valor=?, data_atualizacao=? WHERE id=?",
            (valor, data, id),
        )
        conn.commit()
        conn.close()
        print(f"Valor de mercado ID {id} atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar valor de mercado: {e}")


def deletar_valor_mercado(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM valores_mercado WHERE id=?", (id,))
        conn.commit()
        conn.close()
        print(f"OK: Valor de mercado ID {id} deletado com sucesso!")
    except Exception as e:
        print(f"Erro: Erro ao deletar valor de mercado: {e}")


# Função para buscar jogador por ID
def buscar_jogador_por_id(jogador_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jogadores WHERE id = ?", (jogador_id,))
        jogador = cursor.fetchone()
        conn.close()
        return jogador
    except Exception as e:
        print(f"Erro: Não foi possível buscar o jogador: {e}")
        return None

# Função para listar jogadores com estatísticas
def listar_jogadores_com_estatisticas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT j.id, j.nome, j.idade, j.posicao, c.nome AS clube, e.jogos, e.gols, e.assistencias, e.minutos_jogados, e.cartoes_amarelos, e.cartoes_vermelhos
            FROM jogadores j
            LEFT JOIN clubes c ON j.clube_id = c.id
            LEFT JOIN estatisticas e ON j.id = e.jogador_id
            """
        )
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception as e:
        print(f"Erro: Não foi possível listar jogadores com estatísticas: {e}")
        return []
