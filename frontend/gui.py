import tkinter as tk
from tkinter import ttk, messagebox

from backend.crud import (
    atualizar_clube,
    atualizar_estatistica,
    atualizar_jogador,
    atualizar_valor_mercado,
    criar_clube,
    criar_estatistica,
    criar_jogador,
    criar_valor_mercado,
    deletar_clube,
    deletar_estatistica,
    deletar_jogador,
    deletar_valor_mercado,
    listar_analise_mercado,
    listar_clubes,
    listar_estatisticas,
    listar_jogadores,
    listar_jogadores_por_clube,
    listar_valores_mercado,
)


def format_clube_option(clube):
    return f"{clube[0]} - {clube[1]}" if clube else ""


def carregar_clubes_combobox():
    clubes = listar_clubes()
    options = [format_clube_option(clube) for clube in clubes]
    return options if options else ["Nenhum clube disponível"]


def carregar_jogadores_combobox():
    jogadores = listar_jogadores()
    options = [f"{jog[0]} - {jog[1]}" for jog in jogadores]
    return options if options else ["Nenhum jogador disponível"]


def selecionar_item_tree(tree):
    selected = tree.selection()
    return tree.item(selected[0], "values") if selected else None


def validar_inteiro(valor, nome):
    try:
        return int(valor)
    except ValueError:
        raise ValueError(f"O campo '{nome}' deve ser um número inteiro.")


def validar_float(valor, nome):
    try:
        return float(valor)
    except ValueError:
        raise ValueError(f"O campo '{nome}' deve ser um número decimal.")


def atualizar_treeview(tree, dados, widths=None):
    tree.delete(*tree.get_children())
    for item in dados:
        tree.insert("", tk.END, values=item)
    if widths:
        for col, width in zip(tree["columns"], widths):
            tree.column(col, width=width)


def criar_gui():
    root = tk.Tk()
    root.title("Gestão de Futebol")
    root.geometry("920x540")
    root.minsize(880, 500)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    style = ttk.Style(root)
    style.configure("Treeview.Heading", font=("Segoe UI", 10))
    style.configure("Treeview", font=("Segoe UI", 10))
    style.configure("TButton", padding=6)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    def criar_aba(texto):
        frame = ttk.Frame(notebook, padding=(12, 12, 12, 12))
        notebook.add(frame, text=texto)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        return frame

    frame_clubes = criar_aba("Clubes")
    frame_jogadores = criar_aba("Jogadores")
    frame_estatisticas = criar_aba("Estatísticas")
    frame_valores = criar_aba("Valores")

    def criar_painel_lateral(frame):
        painel = ttk.LabelFrame(frame, text="Dados")
        painel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        painel.columnconfigure(1, weight=1)
        return painel

    def criar_tabela(frame, colunas, headings):
        tabela = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")
        for coluna, titulo in zip(colunas, headings):
            tabela.heading(coluna, text=titulo)
            tabela.column(coluna, anchor="w")
        tabela.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        return tabela

    # ------- Clubes -------
    painel_clubes = criar_painel_lateral(frame_clubes)
    for i, texto in enumerate(["Nome:", "País:", "Ano Fundação:", "Títulos:"]):
        ttk.Label(painel_clubes, text=texto).grid(row=i, column=0, sticky="w", pady=4)
    clube_nome = ttk.Entry(painel_clubes)
    clube_pais = ttk.Entry(painel_clubes)
    clube_ano = ttk.Entry(painel_clubes)
    clube_titulos = ttk.Entry(painel_clubes)
    clube_nome.grid(row=0, column=1, sticky="ew", pady=4)
    clube_pais.grid(row=1, column=1, sticky="ew", pady=4)
    clube_ano.grid(row=2, column=1, sticky="ew", pady=4)
    clube_titulos.grid(row=3, column=1, sticky="ew", pady=4)

    clube_id_var = tk.IntVar(value=0)
    ttk.Label(painel_clubes, text="Clube selecionado:").grid(row=4, column=0, sticky="w", pady=4)
    clube_combo = ttk.Combobox(painel_clubes, state="readonly")
    clube_combo.grid(row=4, column=1, sticky="ew", pady=4)

    botoes_clubes = ttk.Frame(painel_clubes)
    botoes_clubes.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
    for texto, comando in [
        ("Criar", lambda: criar_clube_gui()),
        ("Atualizar", lambda: atualizar_clube_gui()),
        ("Deletar", lambda: deletar_clube_gui()),
        ("Selecionar", lambda: selecionar_clube()),
    ]:
        btn = ttk.Button(botoes_clubes, text=texto, command=comando)
        btn.pack(side="left", expand=True, fill="x", padx=3)

    tabela_clubes_frame = ttk.Frame(frame_clubes)
    tabela_clubes_frame.grid(row=0, column=1, sticky="nsew")
    tabela_clubes_frame.rowconfigure(0, weight=1)
    tabela_clubes_frame.columnconfigure(0, weight=1)
    clube_tree = criar_tabela(
        tabela_clubes_frame,
        ["id", "nome", "pais", "ano", "titulos"],
        ["ID", "Nome", "País", "Ano", "Títulos"],
    )

    elenco_frame = ttk.LabelFrame(frame_clubes, text="Elenco do clube")
    elenco_frame.grid(row=1, column=1, sticky="nsew", pady=(10, 0))
    elenco_frame.rowconfigure(0, weight=1)
    elenco_frame.columnconfigure(0, weight=1)
    elenco_tree = criar_tabela(
        elenco_frame,
        ["id", "nome", "idade", "posicao"],
        ["ID", "Nome", "Idade", "Posição"],
    )
    frame_clubes.columnconfigure(1, weight=1)
    frame_clubes.rowconfigure(1, weight=1)

    def atualizar_elenco_clube(clube_id=None):
        if clube_id is None:
            clube_id = clube_id_var.get() or None

        dados = listar_jogadores_por_clube(clube_id) if clube_id else []
        atualizar_treeview(elenco_tree, dados, widths=[50, 220, 80, 120])

    def carregar_clubes():
        atualizar_treeview(clube_tree, listar_clubes(), widths=[50, 220, 150, 90, 90])
        clube_combo["values"] = carregar_clubes_combobox()
        jogador_clube_combo["values"] = carregar_clubes_combobox()
        atualizar_elenco_clube()

    def selecionar_clube():
        item = selecionar_item_tree(clube_tree)
        if not item:
            messagebox.showwarning("Atenção", "Selecione um clube.")
            return
        clube_id_var.set(item[0])
        clube_nome.delete(0, tk.END)
        clube_nome.insert(0, item[1])
        clube_pais.delete(0, tk.END)
        clube_pais.insert(0, item[2])
        clube_ano.delete(0, tk.END)
        clube_ano.insert(0, item[3])
        clube_titulos.delete(0, tk.END)
        clube_titulos.insert(0, item[4])
        clube_combo.set(f"{item[0]} - {item[1]}")
        atualizar_elenco_clube(int(item[0]))

    def criar_clube_gui():
        try:
            nome = clube_nome.get().strip()
            pais = clube_pais.get().strip()
            ano = validar_inteiro(clube_ano.get().strip(), "Ano Fundação")
            titulos = validar_inteiro(clube_titulos.get().strip(), "Títulos")
            if not nome:
                raise ValueError("O campo 'Nome' é obrigatório.")
            criar_clube(nome, pais, ano, titulos)
            messagebox.showinfo("Sucesso", "Clube criado com sucesso.")
            carregar_clubes()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def atualizar_clube_gui():
        try:
            id_clube = clube_id_var.get()
            if not id_clube:
                raise ValueError("Selecione um clube para atualizar.")
            nome = clube_nome.get().strip()
            pais = clube_pais.get().strip()
            ano = validar_inteiro(clube_ano.get().strip(), "Ano Fundação")
            titulos = validar_inteiro(clube_titulos.get().strip(), "Títulos")
            atualizar_clube(id_clube, nome, pais, ano, titulos)
            messagebox.showinfo("Sucesso", "Clube atualizado com sucesso.")
            carregar_clubes()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def deletar_clube_gui():
        try:
            item = selecionar_item_tree(clube_tree)
            if not item:
                raise ValueError("Selecione um clube para deletar.")
            if messagebox.askyesno("Confirmar", "Deseja deletar o clube selecionado?"):
                deletar_clube(int(item[0]))
                clube_id_var.set(0)
                messagebox.showinfo("Sucesso", "Clube deletado com sucesso.")
                carregar_clubes()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # ------- Jogadores -------
    painel_jogadores = criar_painel_lateral(frame_jogadores)
    for i, texto in enumerate(["Nome:", "Idade:", "Posição:", "Clube:"]):
        ttk.Label(painel_jogadores, text=texto).grid(row=i, column=0, sticky="w", pady=4)
    jogador_nome = ttk.Entry(painel_jogadores)
    jogador_idade = ttk.Entry(painel_jogadores)
    jogador_posicao = ttk.Entry(painel_jogadores)
    jogador_clube_combo = ttk.Combobox(painel_jogadores, values=carregar_clubes_combobox(), state="readonly")
    jogador_nome.grid(row=0, column=1, sticky="ew", pady=4)
    jogador_idade.grid(row=1, column=1, sticky="ew", pady=4)
    jogador_posicao.grid(row=2, column=1, sticky="ew", pady=4)
    jogador_clube_combo.grid(row=3, column=1, sticky="ew", pady=4)

    botoes_jogadores = ttk.Frame(painel_jogadores)
    botoes_jogadores.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
    for texto, comando in [
        ("Criar", lambda: criar_jogador_gui()),
        ("Atualizar", lambda: atualizar_jogador_gui()),
        ("Deletar", lambda: deletar_jogador_gui()),
        ("Selecionar", lambda: selecionar_jogador()),
    ]:
        btn = ttk.Button(botoes_jogadores, text=texto, command=comando)
        btn.pack(side="left", expand=True, fill="x", padx=3)

    tabela_jogadores_frame = ttk.Frame(frame_jogadores)
    tabela_jogadores_frame.grid(row=0, column=1, sticky="nsew")
    tabela_jogadores_frame.rowconfigure(0, weight=1)
    tabela_jogadores_frame.columnconfigure(0, weight=1)
    jogador_tree = criar_tabela(
        tabela_jogadores_frame,
        ["id", "nome", "idade", "posicao", "clube"],
        ["ID", "Nome", "Idade", "Posição", "Clube"],
    )
    frame_jogadores.columnconfigure(1, weight=1)

    jogador_id_var = tk.IntVar(value=0)

    def carregar_jogadores():
        atualizar_treeview(jogador_tree, listar_jogadores(), widths=[50, 220, 80, 120, 180])
        jogador_clube_combo["values"] = carregar_clubes_combobox()
        stat_jogador_combo["values"] = carregar_jogadores_combobox()
        valor_jogador_combo["values"] = carregar_jogadores_combobox()

    def selecionar_jogador():
        item = selecionar_item_tree(jogador_tree)
        if not item:
            messagebox.showwarning("Atenção", "Selecione um jogador.")
            return
        jogador_id_var.set(item[0])
        jogador_nome.delete(0, tk.END)
        jogador_nome.insert(0, item[1])
        jogador_idade.delete(0, tk.END)
        jogador_idade.insert(0, item[2])
        jogador_posicao.delete(0, tk.END)
        jogador_posicao.insert(0, item[3])
        jogador_clube_combo.set(item[4] if item[4] else "Nenhum clube disponível")

    def criar_jogador_gui():
        try:
            nome = jogador_nome.get().strip()
            idade = validar_inteiro(jogador_idade.get().strip(), "Idade")
            posicao = jogador_posicao.get().strip()
            clube_text = jogador_clube_combo.get().strip()
            clube_id = int(clube_text.split(" - ")[0]) if " - " in clube_text else None
            if not nome:
                raise ValueError("O campo 'Nome' é obrigatório.")
            criar_jogador(nome, idade, posicao, clube_id)
            messagebox.showinfo("Sucesso", "Jogador criado com sucesso.")
            carregar_jogadores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def atualizar_jogador_gui():
        try:
            id_jogador = jogador_id_var.get()
            if not id_jogador:
                raise ValueError("Selecione um jogador para atualizar.")
            nome = jogador_nome.get().strip()
            idade = validar_inteiro(jogador_idade.get().strip(), "Idade")
            posicao = jogador_posicao.get().strip()
            clube_text = jogador_clube_combo.get().strip()
            clube_id = int(clube_text.split(" - ")[0]) if " - " in clube_text else None
            atualizar_jogador(id_jogador, nome, idade, posicao, clube_id)
            messagebox.showinfo("Sucesso", "Jogador atualizado com sucesso.")
            carregar_jogadores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def deletar_jogador_gui():
        try:
            item = selecionar_item_tree(jogador_tree)
            if not item:
                raise ValueError("Selecione um jogador para deletar.")
            if messagebox.askyesno("Confirmar", "Deseja deletar o jogador selecionado?"):
                deletar_jogador(int(item[0]))
                messagebox.showinfo("Sucesso", "Jogador deletado com sucesso.")
                carregar_jogadores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # ------- Estatísticas -------
    painel_estatisticas = criar_painel_lateral(frame_estatisticas)
    labels = ["Jogador:", "Jogos:", "Gols:", "Assistências:", "Minutos:", "Amarelos:", "Vermelhos:"]
    for i, texto in enumerate(labels):
        ttk.Label(painel_estatisticas, text=texto).grid(row=i, column=0, sticky="w", pady=4)
    stat_jogador_combo = ttk.Combobox(painel_estatisticas, values=carregar_jogadores_combobox(), state="readonly")
    stat_jogos = ttk.Entry(painel_estatisticas)
    stat_gols = ttk.Entry(painel_estatisticas)
    stat_assist = ttk.Entry(painel_estatisticas)
    stat_minutos = ttk.Entry(painel_estatisticas)
    stat_amarelos = ttk.Entry(painel_estatisticas)
    stat_vermelhos = ttk.Entry(painel_estatisticas)

    stat_jogador_combo.grid(row=0, column=1, sticky="ew", pady=4)
    stat_jogos.grid(row=1, column=1, sticky="ew", pady=4)
    stat_gols.grid(row=2, column=1, sticky="ew", pady=4)
    stat_assist.grid(row=3, column=1, sticky="ew", pady=4)
    stat_minutos.grid(row=4, column=1, sticky="ew", pady=4)
    stat_amarelos.grid(row=5, column=1, sticky="ew", pady=4)
    stat_vermelhos.grid(row=6, column=1, sticky="ew", pady=4)

    botoes_estatisticas = ttk.Frame(painel_estatisticas)
    botoes_estatisticas.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
    for texto, comando in [
        ("Criar", lambda: criar_estatistica_gui()),
        ("Selecionar", lambda: selecionar_estatistica()),
        ("Atualizar", lambda: atualizar_estatistica_gui()),
        ("Deletar", lambda: deletar_estatistica_gui()),
    ]:
        btn = ttk.Button(botoes_estatisticas, text=texto, command=comando)
        btn.pack(side="left", expand=True, fill="x", padx=3)

    tabela_estatisticas_frame = ttk.Frame(frame_estatisticas)
    tabela_estatisticas_frame.grid(row=0, column=1, sticky="nsew")
    tabela_estatisticas_frame.rowconfigure(0, weight=1)
    tabela_estatisticas_frame.columnconfigure(0, weight=1)
    estat_tree = criar_tabela(
        tabela_estatisticas_frame,
        ["id", "jogador", "jogos", "gols", "assist", "minutos", "amarelos", "vermelhos"],
        ["ID", "Jogador", "Jogos", "Gols", "Assistências", "Minutos", "Amarelos", "Vermelhos"],
    )
    frame_estatisticas.columnconfigure(1, weight=1)

    def carregar_estatisticas():
        atualizar_treeview(estat_tree, listar_estatisticas(), widths=[50, 180, 80, 80, 120, 90, 90, 90])

    def selecionar_estatistica():
        item = selecionar_item_tree(estat_tree)
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma estatística.")
            return
        jogador_text = next((opt for opt in carregar_jogadores_combobox() if opt.endswith(f" - {item[1]}")), item[1])
        stat_jogador_combo.set(jogador_text)
        stat_jogos.delete(0, tk.END)
        stat_jogos.insert(0, item[2])
        stat_gols.delete(0, tk.END)
        stat_gols.insert(0, item[3])
        stat_assist.delete(0, tk.END)
        stat_assist.insert(0, item[4])
        stat_minutos.delete(0, tk.END)
        stat_minutos.insert(0, item[5])
        stat_amarelos.delete(0, tk.END)
        stat_amarelos.insert(0, item[6])
        stat_vermelhos.delete(0, tk.END)
        stat_vermelhos.insert(0, item[7])

    def criar_estatistica_gui():
        try:
            jogador_text = stat_jogador_combo.get().strip()
            if " - " not in jogador_text:
                raise ValueError("Selecione um jogador válido.")
            jogador_id = int(jogador_text.split(" - ")[0])
            jogos = validar_inteiro(stat_jogos.get().strip(), "Jogos")
            gols = validar_inteiro(stat_gols.get().strip(), "Gols")
            assist = validar_inteiro(stat_assist.get().strip(), "Assistências")
            minutos = validar_inteiro(stat_minutos.get().strip(), "Minutos")
            amarelos = validar_inteiro(stat_amarelos.get().strip(), "Amarelos")
            vermelhos = validar_inteiro(stat_vermelhos.get().strip(), "Vermelhos")
            criar_estatistica(jogador_id, jogos, gols, assist, minutos, amarelos, vermelhos)
            messagebox.showinfo("Sucesso", "Estatística criada com sucesso.")
            carregar_estatisticas()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def atualizar_estatistica_gui():
        try:
            jogador_text = stat_jogador_combo.get().strip()
            if " - " not in jogador_text:
                raise ValueError("Selecione um jogador válido.")
            jogador_id = int(jogador_text.split(" - ")[0])
            jogos = validar_inteiro(stat_jogos.get().strip(), "Jogos")
            gols = validar_inteiro(stat_gols.get().strip(), "Gols")
            assist = validar_inteiro(stat_assist.get().strip(), "Assistências")
            minutos = validar_inteiro(stat_minutos.get().strip(), "Minutos")
            amarelos = validar_inteiro(stat_amarelos.get().strip(), "Amarelos")
            vermelhos = validar_inteiro(stat_vermelhos.get().strip(), "Vermelhos")
            atualizar_estatistica(jogador_id, jogos, gols, assist, minutos, amarelos, vermelhos)
            messagebox.showinfo("Sucesso", "Estatística atualizada com sucesso.")
            carregar_estatisticas()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def deletar_estatistica_gui():
        try:
            item = selecionar_item_tree(estat_tree)
            if not item:
                raise ValueError("Selecione uma estatística para deletar.")
            jogador_text = stat_jogador_combo.get().strip()
            if " - " not in jogador_text:
                raise ValueError("Selecione um jogador válido para deletar.")
            jogador_id = int(jogador_text.split(" - ")[0])
            if messagebox.askyesno("Confirmar", "Deseja deletar a estatística desse jogador?"):
                deletar_estatistica(jogador_id)
                messagebox.showinfo("Sucesso", "Estatística deletada com sucesso.")
                carregar_estatisticas()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    # ------- Valores -------
    painel_valores = criar_painel_lateral(frame_valores)
    for i, texto in enumerate(["Jogador:", "Valor (milhões):", "Data (YYYY-MM-DD):"]):
        ttk.Label(painel_valores, text=texto).grid(row=i, column=0, sticky="w", pady=4)
    valor_jogador_combo = ttk.Combobox(painel_valores, values=carregar_jogadores_combobox(), state="readonly")
    valor_valor = ttk.Entry(painel_valores)
    valor_data = ttk.Entry(painel_valores)
    valor_jogador_combo.grid(row=0, column=1, sticky="ew", pady=4)
    valor_valor.grid(row=1, column=1, sticky="ew", pady=4)
    valor_data.grid(row=2, column=1, sticky="ew", pady=4)

    botoes_valores = ttk.Frame(painel_valores)
    botoes_valores.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
    for texto, comando in [
        ("Criar", lambda: criar_valor_gui()),
        ("Atualizar", lambda: atualizar_valor_gui()),
        ("Deletar", lambda: deletar_valor_gui()),
        ("Selecionar", lambda: selecionar_valor()),
    ]:
        btn = ttk.Button(botoes_valores, text=texto, command=comando)
        btn.pack(side="left", expand=True, fill="x", padx=3)

    tabela_valores_frame = ttk.Frame(frame_valores)
    tabela_valores_frame.grid(row=0, column=1, sticky="nsew")
    tabela_valores_frame.rowconfigure(0, weight=1)
    tabela_valores_frame.columnconfigure(0, weight=1)
    valor_tree = criar_tabela(tabela_valores_frame, ["id", "jogador", "valor", "data"], ["ID", "Jogador", "Valor", "Data"])

    analise_frame = ttk.LabelFrame(frame_valores, text="Análise de mercado")
    analise_frame.grid(row=1, column=1, sticky="nsew", pady=(10, 0))
    analise_frame.rowconfigure(0, weight=1)
    analise_frame.columnconfigure(0, weight=1)
    analise_tree = criar_tabela(
        analise_frame,
        ["id", "jogador", "clube", "valor", "jogos", "gols", "assistencias", "minutos", "score"],
        ["ID", "Jogador", "Clube", "Valor (M)", "Jogos", "Gols", "Assistências", "Minutos", "Score"],
    )
    frame_valores.columnconfigure(1, weight=1)
    frame_valores.rowconfigure(1, weight=1)

    valor_id_var = tk.IntVar(value=0)

    def carregar_valores():
        atualizar_treeview(valor_tree, listar_valores_mercado(), widths=[50, 220, 120, 120])
        atualizar_treeview(
            analise_tree,
            listar_analise_mercado(),
            widths=[50, 220, 150, 90, 70, 70, 100, 90, 90],
        )

    def selecionar_valor():
        item = selecionar_item_tree(valor_tree)
        if not item:
            messagebox.showwarning("Atenção", "Selecione um valor.")
            return
        valor_id_var.set(item[0])
        jogador_text = next((opt for opt in carregar_jogadores_combobox() if opt.endswith(f" - {item[1]}")), item[1])
        valor_jogador_combo.set(jogador_text)
        valor_valor.delete(0, tk.END)
        valor_valor.insert(0, item[2])
        valor_data.delete(0, tk.END)
        valor_data.insert(0, item[3])

    def criar_valor_gui():
        try:
            jogador_text = valor_jogador_combo.get().strip()
            if " - " not in jogador_text:
                raise ValueError("Selecione um jogador válido.")
            jogador_id = int(jogador_text.split(" - ")[0])
            valor = validar_float(valor_valor.get().strip(), "Valor")
            data = valor_data.get().strip() or None
            criar_valor_mercado(jogador_id, valor, data)
            messagebox.showinfo("Sucesso", "Valor de mercado registrado com sucesso.")
            carregar_valores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def atualizar_valor_gui():
        try:
            id_valor = valor_id_var.get()
            if not id_valor:
                raise ValueError("Selecione um registro para atualizar.")
            valor = validar_float(valor_valor.get().strip(), "Valor")
            data = valor_data.get().strip() or None
            atualizar_valor_mercado(id_valor, valor, data)
            messagebox.showinfo("Sucesso", "Valor de mercado atualizado com sucesso.")
            carregar_valores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    def deletar_valor_gui():
        try:
            item = selecionar_item_tree(valor_tree)
            if not item:
                raise ValueError("Selecione um registro para deletar.")
            if messagebox.askyesno("Confirmar", "Deseja deletar o registro selecionado?"):
                deletar_valor_mercado(int(item[0]))
                messagebox.showinfo("Sucesso", "Registro deletado com sucesso.")
                carregar_valores()
        except Exception as exc:
            messagebox.showerror("Erro", str(exc))

    carregar_clubes()
    carregar_jogadores()
    carregar_estatisticas()
    carregar_valores()

    root.mainloop()
