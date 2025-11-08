from datetime import datetime
import json
import os
from typing import Dict, Any

DATA_FILE = "inventory.json"  # arquivo JSON local


def load_data() -> Dict[str, Any]:
    """Carrega dados do JSON; se não existir, retorna estrutura vazia."""
    if not os.path.exists(DATA_FILE):
        return {"products": {}, "movements": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict[str, Any]) -> None:
    """Salva dados no JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def input_date(prompt: str) -> str:
    """Lê data DD-MM-AAAA; Enter = hoje; repete até ser válida."""
    raw = input(prompt + " (DD-MM-AAAA) [Enter = hoje]: ").strip()
    if not raw:
        return datetime.now().strftime("%d-%m-%Y")
    try:
        dt = datetime.strptime(raw, "%d-%m-%Y")
        return dt.strftime("%d-%m-%Y")
    except ValueError:
        print("Data inválida. Use DD-MM-AAAA. Tente novamente.")
        return input_date(prompt)


def input_positive_int(prompt: str) -> int:
    """Lê inteiro > 0; repete até ser válido."""
    raw = input(prompt + ": ").strip()
    if not raw.isdigit() or int(raw) <= 0:
        print("Informe um número inteiro positivo.")
        return input_positive_int(prompt)
    return int(raw)


def registrar_entrada(data_store: Dict[str, Any]) -> None:
    """Registra ENTRADA: valida produto, soma estoque e grava movimento."""
    products = data_store["products"]
    if not products:
        print("⚠ Nenhum produto cadastrado. Cadastre um produto primeiro.")
        return
    listar_produtos(data_store)
    cod = input("Informe o CÓDIGO do produto para entrada: ").strip()
    if cod not in products:
        print("Produto não encontrado.")
        return
    qty = input_positive_int("Quantidade recebida")
    data_mov = input_date("Data de entrada")
    responsavel = input("Responsável pela entrada: ").strip() or "N/D"

    products[cod]["stock"] += qty
    data_store["movements"].append({
        "type": "ENTRADA",
        "product_code": cod,
        "product_name": products[cod]["name"],
        "quantity": qty,
        "date": data_mov,
        "responsible": responsavel,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })
    save_data(data_store)
    print(f"✅ Entrada registrada. Novo saldo de '{products[cod]['name']}': {products[cod]['stock']}")


def registrar_saida(data_store: Dict[str, Any]) -> None:
    """Registra SAÍDA: valida produto/saldo, subtrai estoque e grava movimento."""
    products = data_store["products"]
    if not products:
        print("⚠ Nenhum produto cadastrado. Cadastre um produto primeiro.")
        return
    listar_produtos(data_store)
    cod = input("Informe o CÓDIGO do produto para saída: ").strip()
    if cod not in products:
        print("Produto não encontrado.")
        return
    qty = input_positive_int("Quantidade a retirar")
    estoque_atual = products[cod]["stock"]
    if qty > estoque_atual:
        print(f"❌ Saldo insuficiente. Estoque atual: {estoque_atual}.")
        return
    data_mov = input_date("Data da saída")
    responsavel = input("Responsável pela saída: ").strip() or "N/D"

    products[cod]["stock"] -= qty
    data_store["movements"].append({
        "type": "SAIDA",
        "product_code": cod,
        "product_name": products[cod]["name"],
        "quantity": qty,
        "date": data_mov,
        "responsible": responsavel,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })
    save_data(data_store)
    print(f"✅ Saída registrada. Novo saldo de '{products[cod]['name']}': {products[cod]['stock']}")


def cadastrar_produto(data_store: Dict[str, Any]) -> None:
    """Cadastra produto novo com estoque inicial."""
    cod = input("Código do produto (único): ").strip()
    if not cod:
        print("Código não pode ser vazio.")
        return
    if cod in data_store["products"]:
        print("Já existe produto com esse código.")
        return
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return
    estoque_inicial = input_positive_int("Estoque inicial")

    data_store["products"][cod] = {"name": nome, "stock": estoque_inicial}
    save_data(data_store)
    print(f"✅ Produto '{nome}' cadastrado com saldo {estoque_inicial}.")


def listar_produtos(data_store: Dict[str, Any]) -> None:
    """Lista produtos e saldos."""
    products = data_store["products"]
    if not products:
        print("(sem produtos)")
        return
    print("\n=== PRODUTOS ===")
    for cod, p in products.items():
        print(f"- {cod} | {p['name']} | saldo: {p['stock']}")
    print("")


def listar_movimentacoes(data_store: Dict[str, Any]) -> None:
    """Lista últimas movimentações (até 100)."""
    movs = data_store["movements"]
    if not movs:
        print("(sem movimentações)")
        return
    print("\n=== MOVIMENTAÇÕES ===")
    for m in movs[-100:]:
        print(f"[{m['type']}] {m['date']} • {m['product_code']} - {m['product_name']} • "
              f"qty={m['quantity']} • resp={m['responsible']} • criado={m['created_at']}")
    print("")


def menu():
    """Menu CLI principal."""
    data_store = load_data()
    while True:
        print(
            "\n"
            "╔══════════════════════════════════════╗\n"
            "║          CONTROLE DE ESTOQUE         ║\n"
            "╠══════════════════════════════════════╣\n"
            "║ 1 ▸ Cadastrar produto                ║\n"
            "║ 2 ▸ Registrar ENTRADA                ║\n"
            "║ 3 ▸ Registrar SAÍDA                  ║\n"
            "║ 4 ▸ Listar produtos                  ║\n"
            "║ 5 ▸ Listar movimentações             ║\n"
            "║ 0 ▸ Sair                             ║\n"
            "╚══════════════════════════════════════╝"
        )
        op = input("Escolha uma opção: ").strip()
        if op == "1":
            cadastrar_produto(data_store)
        elif op == "2":
            registrar_entrada(data_store)
        elif op == "3":
            registrar_saida(data_store)
        elif op == "4":
            listar_produtos(data_store)
        elif op == "5":
            listar_movimentacoes(data_store)
        elif op == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
