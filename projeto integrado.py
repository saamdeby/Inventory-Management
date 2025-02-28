import sqlite3
from datetime import datetime

# Conectar ao banco de dados ou criar um novo
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    localizacao TEXT,
    quantidade INTEGER NOT NULL,
    quantidade_minima INTEGER NOT NULL
)
''')

# Criar tabela de movimentação se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    tipo TEXT,
    quantidade INTEGER,
    data TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')


def a_produto():
    while True:
        nome = input("Digite o nome do novo produto: ")
        if nome.strip():
            break
        else:
            print("Nome invalido. Tente novamente\n")

    while True:
        try:
            quantidade = int(input("Digite a quantidade do novo produto: "))
            if quantidade > 0:
                break
        except ValueError:
            print("Quantidade invalida. Tente novamente\n")

    while True:
        localizacao = input("Digite a localização do novo produto: ")
        if localizacao.strip():
            break
        else:
            print("Localização invalida. Tente novamente\n")

    while True:
        descricao = input("Digite a descricao do novo produto: ")
        if descricao.strip():
            break
        else:
            print("Descricao invalida. Tente novamente\n")

    while True:
        try:
            quantidade_minima = int(
                input("Digite a quantidade_minima do novo produto: "))
            if quantidade > 0:
                break
        except ValueError:
            print("Quantidade invalida. Tente novamente\n")

    cursor.execute('''
    INSERT INTO produtos (nome, descricao, localizacao, quantidade, quantidade_minima)
    VALUES (?, ?, ?, ?, ?)
    ''', (nome, descricao, localizacao, quantidade, quantidade_minima))
    conn.commit()
    print(f"\nProduto '{nome}' adicionado com sucesso!\n")


def b_produto():
    print("Registro de produtos")
    try:
        produto_id = int(
            input("Digite o ID do produto, para criar um registro: "))
    except ValueError:
        print("ID invalido. Digite um ID existente !")
        return

        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Produto com ID {produto_id} não encontrado")
            return produto_id

    while True:
        try:
            quantidade = int(input("Digite quanto será adicionado: "))
            if quantidade <= 0:
                print("A quantidade deve ser um numero positivo e inteiro! ")
                continue
            break
        except ValueError:
            print("Valor invalido, digite novamente! ")

# Atualizar a quantidade de produtos
    cursor.execute("""
  UPDATE produtos
  SET quantidade = quantidade + ?
  WHERE id = ?
  """, (quantidade, produto_id))

# Registrar a movimentação
    cursor.execute("""
  INSERT INTO movimentacao (produto_id, tipo, quantidade, data)
  VALUES (?, 'entrada', ?, ?)
  """, (produto_id, quantidade, datetime.now()))

    conn.commit()
    print(f"\nEntrada no valor de {quantidade} unidades no produto ID {
          produto_id} registrada com sucesso!\n")


def saida_produto():
    print("\n-- Registrar Saída de Produtos --")
    try:
        produto_id = int(
            input("Digite o ID do produto, para registrar uma saída: "))
    except ValueError:
        print("ID invalido. Por favor digite um ID existente !")
        return
    cursor.execute("SELECT nome FROM produtos WHERE id = ?", (produto_id,))
    resultado = cursor.fetchone()
    if not resultado:
        print(f"Produto com ID {produto_id} não encontrado")
        return
        nome_produto, estoque_atual = resultado[0], resultado[1]
        print(f"\nProduto: {nome_produto}")
        print(f"Estoque atual: {estoque_atual}")
        while True:
            try:
                quantidade = int(input("Digite a quantidade a ser retirada: "))
                if quantidade <= 0:
                    print("A quantidade deve ser um número positivo. Tente Novamente ")
                    continue
                if quantidade > estoque_atual:
                    print(f"Não há unidades suficientes de {
                          nome_produto}. Estoque atual: {estoque_atual}")
                    continue
                break
            except ValueError:
                print("Valor invalido, digite novamente! ")

    conn.commit()


def gerar_rlt_movimentacao():
    print("\n=== Relatório de Movimentação ===")
    cursor.execute('''
    SELECT m.id, p.nome, m.tipo, m.quantidade, m.data
    FROM movimetacao m
    JOIN produtos p ON m.produtos_id = p.id
    ORDER BY m.data DESC
    ''')

    movimentacoes = cursor.fetchall()

    if not movimentacoes:
        print("\nNenhuma movimentção registrada. \n")
        return

    # Formatção e exibição de resultado

    print(f"{'ID':<5} {'Produto':<30} {'Tipo':<10} {
          'Quantidade':<10} {'Data':<25}")
    print("-" * 80)
    for mov in movimentacoes:
        id_mov, nome, tipo, quantidade, data = mov
        print(f"{id_mov:<5} {nome:<30} {tipo:<10} {quantidade:<10} {data:<25}")
    print()


def listar_produtos():
    cursor.execute(
        'SELECT id, nome, descricao, localizacao, quantidade, quantidade_minima FROM produtos')
    produtos = cursor.fetchall()

    if not produtos:
        print("\nNenhum produto cadastrado.\n")
        return

    print("\n____Lista de Produtos____")
    header = f"{'ID':<5} {'Nome':20} {'Descrição':<30} {
        'Localização':<20} {'Quantidade':<20} {'Estoque Mínimo':<15}"
    print(header)
    print("-" * len(header))
    for produto in produtos:
        id_prod, nome, descricao, localizacao, quantidade, quantidade_minima = produto
        descricao_curta = (
            descricao[:27] + '...') if len(descricao) > 30 else descricao
        print(f"{id_prod:<5} {nome:<20} {descricao_curta:<30} {
              localizacao:<20} {quantidade:<20} {quantidade_minima:<15}")
    print()


def quantidade_minima():

    def quantidade_minima():

        cursor.execute('''
    SELECT nome, quantidade_minima, quantidade
FROM produtos
WHERE quantidade < quantidade_minima;

    ''')

    produtos_baixo_estoque = cursor.fetchall()
    print(produtos_baixo_estoque)

    if produtos_baixo_estoque:
        print(f"{'Produto':<15} {'Quantidade_minima':<30} {'Quantidade':<30}")
        print("-" * 70)
        for produto in produtos_baixo_estoque:
            nome, quantidade_minima, quantidade = produto
            print(f"{nome:<15} {quantidade_minima:<30} {quantidade:<30}")
        print()
        if quantidade < quantidade_minima:
            print("Esses produtos estão com estoque abaixo do mínimo.")

    else:
        print("Todos os produtos estão com estoque acima do mínimo.")


def deletar_produto(id):
    """Deleta um produto do banco de dados."""
    try:
        delete_id = int(input("ID do produto a ser buscado: ").strip())
    except ValueError:
        print("ID invalido. Digite um ID existente !")
        return

    cursor.execute('''DELETE FROM produtos WHERE id=?''', (delete_id,))
    delete = cursor.fetchone()
    if not delete:
        print(f"\nProduto com ID {delete_id} não encontrado.\n")
        return delete_id
    else:
        print(f"\nProduto com ID {delete_id} deletado com sucesso!\n")
        conn.commit()


def buscar_produto(id):
    """Busca e exibe um produto específico pelo ID."""
    try:
        buscar_id = int(input("ID do produto a ser buscado: ").strip())
    except ValueError:
        print("ID invalido. Digite um ID existente !")
        return

    cursor.execute("SELECT * FROM produtos WHERE id=?", (buscar_id,))
    buscar = cursor.fetchone()
    if not buscar:
        print(f"\nProduto com ID {buscar_id} não encontrado.\n")
        return buscar_id
    else:
        print(f"\nProduto com ID {buscar_id} deletado com sucesso!\n")
        conn.commit()

    if buscar:
        print("\nID | Nome | Descrição | Preço | Quantidade")
        print("--------------------------------------------")
        print(f"{buscar[0]} | {buscar[1]} | {buscar[2]} | R${
              buscar[3]:.2f} | {buscar[4]}\n")
    else:
        print(f"\nProduto com ID {id} não encontrado.\n")

        conn.commit()


def mostrar_menu():
    while True:
        try:
            print("Menu:")
            print("1. Adicionar produto")
            print("2. Entrada produto")
            print("3. Saida produto")
            print("4. Relatorio de movimentação")
            print("5. Quantidade mínima")
            print("6. Listar produtos")
            print("7. Deletar produto")
            print("8. Buscar produto")
            print("9. Sair")
            menu = int(input("Digite a opção desejada (1 a 9): "))
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

# Retorna ao início do loop para tentar novamente
        if menu == 1:
            print("Opção 1 selecionada: Adicionar produto")
            a_produto()

        elif menu == 2:
            b_produto()
            print("Opção 2 selecionada: Entrada de produto")

        elif menu == 3:
            print("Opção 3 selecionada: Saida de produto")
            saida_produto()

        elif menu == 4:
            print("Opção 4 selecionada: Relatorio de movimentação")
            gerar_rlt_movimentacao()

        elif menu == 5:
            quantidade_minima()
            print("Opção 5 selecionada: Quantidade_minima")

        elif menu == 6:
            listar_produtos()
            print("Opção 6 selecionada: Listar Produtos")

        elif menu == 7:
            deletar_produto(id)
            print("Opção 7 selecionada: Deletar Produto")

        elif menu == 8:
            buscar_produto(id)
            print("Opção 8 selecionada: Buscar Produto")

        elif menu == 9:
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")


if __name__ == "__main__":
    try:
        mostrar_menu()
    finally:
        # Fechar conexão com o banco de dados ao encerrar o programa
        conn.close()
