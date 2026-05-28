import sqlite3
import os
from typing import Optional


NOME_BANCO = "estoque.db"
UNIDADES_VALIDAS = {"un", "kg", "g", "L", "mL", "m", "cm", "cx", "pç"}


def criar_banco() -> None:
    if not os.path.exists(NOME_BANCO):
        print("Banco não encontrado. Criando banco...")
    else:
        print("Banco encontrado. Abrindo sistema...")

    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                codigo      TEXT    PRIMARY KEY,
                nome_item   TEXT    NOT NULL,
                quantidade  REAL    NOT NULL,
                unidade     TEXT    NOT NULL,
                preco_unit  REAL    NOT NULL,
                valor_total REAL    NOT NULL
            )
        """)

    print("Banco pronto!\n")


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(NOME_BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def exibir_produto(produto: sqlite3.Row) -> None:
    print(f"""
Código:         {produto['codigo']}
Produto:        {produto['nome_item']}
Quantidade:     {produto['quantidade']} {produto['unidade']}
Preço Unitário: R$ {produto['preco_unit']:.2f}
Valor Total:    R$ {produto['valor_total']:.2f}
----------------------------------------
""")


def validar_codigo(codigo: str) -> bool:
    return codigo.isdigit() and len(codigo) == 3


def cadastrar_produto() -> None:
    print("\n=== CADASTRO DE PRODUTO ===")

    codigo = input("Código do produto (001-999): ").strip()

    if not validar_codigo(codigo):
        print("Código inválido.")
        return

    nome = input("Nome do produto: ").strip()

    quantidade = float(input("Quantidade: "))
    unidade = input("Unidade de medida: ")
    preco = float(input("Preço unitário: R$ "))

    valor_total = quantidade * preco

    with conectar() as conexao:
        try:
            conexao.execute("""
                INSERT INTO estoque
                (codigo, nome_item, quantidade, unidade, preco_unit, valor_total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, nome, quantidade, unidade, preco, valor_total))

            print("\nProduto cadastrado com sucesso!")

        except sqlite3.IntegrityError:
            print("Já existe um produto com esse código.")


def listar_produtos() -> None:
    print("\n=== LISTA DE PRODUTOS ===")

    with conectar() as conexao:
        produtos = conexao.execute(
            "SELECT * FROM estoque ORDER BY nome_item"
        ).fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        exibir_produto(produto)


def buscar_produto() -> None:
    codigo = input("Digite o código do produto: ")

    with conectar() as conexao:
        produto = conexao.execute(
            "SELECT * FROM estoque WHERE codigo = ?",
            (codigo,)
        ).fetchone()

    if produto:
        exibir_produto(produto)
    else:
        print("Produto não encontrado.")


def editar_produto() -> None:
    codigo = input("Código do produto para editar: ")

    with conectar() as conexao:
        cursor = conexao.cursor()

        produto = cursor.execute(
            "SELECT * FROM estoque WHERE codigo = ?",
            (codigo,)
        ).fetchone()

        if not produto:
            print("Produto não encontrado.")
            return

        novo_nome = input("Novo nome: ")
        nova_quantidade = float(input("Nova quantidade: "))
        nova_unidade = input("Nova unidade: ")
        novo_preco = float(input("Novo preço: "))

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

        print("Produto atualizado com sucesso!")


def excluir_produto() -> None:
    codigo = input("Código do produto para excluir: ")

    with conectar() as conexao:
        cursor = conexao.cursor()

        produto = cursor.execute(
            "SELECT * FROM estoque WHERE codigo = ?",
            (codigo,)
        ).fetchone()

        if not produto:
            print("Produto não encontrado.")
            return

        cursor.execute(
            "DELETE FROM estoque WHERE codigo = ?",
            (codigo,)
        )

        print("Produto removido com sucesso!")


def menu():
    criar_banco()

    while True:
        print("""
===== SISTEMA DE ESTOQUE =====

1 - Cadastrar produto
2 - Listar produtos
3 - Buscar produto
4 - Editar produto
5 - Excluir produto
6 - Sair
""")

        opcao = input("Escolha uma opção: ")

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
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()