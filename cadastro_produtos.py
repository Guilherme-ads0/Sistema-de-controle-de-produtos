import sqlite3

# ==============================
# BANCO DE DADOS
# ==============================

conexao = sqlite3.connect("estoque.db")
conexao.row_factory = sqlite3.Row

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estoque (
    codigo TEXT PRIMARY KEY,
    nome_item TEXT NOT NULL,
    quantidade REAL NOT NULL,
    unidade TEXT NOT NULL,
    preco_unit REAL NOT NULL,
    valor_total REAL NOT NULL
)
""")

conexao.commit()


# ==============================
# FUNÇÕES
# ==============================

def exibir_produto(produto):
    print(f"""
Código: {produto['codigo']}
Produto: {produto['nome_item']}
Quantidade: {produto['quantidade']} {produto['unidade']}
Preço Unitário: R$ {produto['preco_unit']:.2f}
Valor Total: R$ {produto['valor_total']:.2f}
------------------------------
""")


def cadastrar_produto():
    print("\n=== CADASTRO DE PRODUTO ===")

    codigo = input("Código do produto: ").strip()
    nome = input("Nome do produto: ").strip()

    try:
        quantidade = float(input("Quantidade: "))
        unidade = input("Unidade de medida: ").strip()
        preco = float(input("Preço unitário: R$ "))
    except ValueError:
        print("Digite números válidos.")
        return

    valor_total = quantidade * preco

    try:
        cursor.execute("""
        INSERT INTO estoque
        (codigo, nome_item, quantidade, unidade, preco_unit, valor_total)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            codigo,
            nome,
            quantidade,
            unidade,
            preco,
            valor_total
        ))

        conexao.commit()

        print("\nProduto cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Já existe um produto com esse código.")


def listar_produtos():
    print("\n=== LISTA DE PRODUTOS ===")

    cursor.execute("""
    SELECT * FROM estoque
    ORDER BY nome_item
    """)

    produtos = cursor.fetchall()

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        exibir_produto(produto)


def buscar_produto():
    print("\n=== BUSCAR PRODUTO ===")

    codigo = input("Digite o código do produto: ").strip()

    cursor.execute("""
    SELECT * FROM estoque
    WHERE codigo = ?
    """, (codigo,))

    produto = cursor.fetchone()

    if produto:
        exibir_produto(produto)
    else:
        print("Produto não encontrado.")


def editar_produto():
    print("\n=== EDITAR PRODUTO ===")

    codigo = input("Código do produto: ").strip()

    cursor.execute("""
    SELECT * FROM estoque
    WHERE codigo = ?
    """, (codigo,))

    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado.")
        return

    novo_nome = input("Novo nome: ").strip()

    try:
        nova_quantidade = float(input("Nova quantidade: "))
        nova_unidade = input("Nova unidade: ").strip()
        novo_preco = float(input("Novo preço: "))
    except ValueError:
        print("Digite números válidos.")
        return

    novo_total = nova_quantidade * novo_preco

    cursor.execute("""
    UPDATE estoque
    SET nome_item = ?,
        quantidade = ?,
        unidade = ?,
        preco_unit = ?,
        valor_total = ?
    WHERE codigo = ?
    """, (
        novo_nome,
        nova_quantidade,
        nova_unidade,
        novo_preco,
        novo_total,
        codigo
    ))

    conexao.commit()

    print("Produto atualizado com sucesso!")


def excluir_produto():
    print("\n=== EXCLUIR PRODUTO ===")

    codigo = input("Código do produto: ").strip()

    cursor.execute("""
    SELECT * FROM estoque
    WHERE codigo = ?
    """, (codigo,))

    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado.")
        return

    cursor.execute("""
    DELETE FROM estoque
    WHERE codigo = ?
    """, (codigo,))

    conexao.commit()

    print("Produto removido com sucesso!")


def relatorio_estoque():
    print("\n=== RELATÓRIO ===")

    cursor.execute("SELECT COUNT(*) FROM estoque")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(valor_total) FROM estoque")
    valor_total = cursor.fetchone()[0]

    if valor_total is None:
        valor_total = 0

    print(f"Total de produtos: {total}")
    print(f"Valor total do estoque: R$ {valor_total:.2f}")


# ==============================
# MENU
# ==============================

while True:
    print("""
===== SISTEMA DE ESTOQUE =====

1 - Cadastrar produto
2 - Listar produtos
3 - Buscar produto
4 - Editar produto
5 - Excluir produto
6 - Relatório
7 - Sair
""")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        cadastrar_produto()

    elif opcao == "2":
        listar_produtos()

    elif opcao == "3":
        buscar_produto()

    elif opcao == "4":
        editar_produto()

    elif opcao == "5":
        excluir_produto()

    elif opcao == "6":
        relatorio_estoque()

    elif opcao == "7":
        print("Sistema encerrado.")
        conexao.close()
        break

    else:
        print("Opção inválida.")
