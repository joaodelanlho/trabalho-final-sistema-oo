from abc import ABC, abstractmethod


# CLASSE ABSTRATA (R1)
class ItemCardapio(ABC):
    def __init__(self, codigo, nome, preco):
        self.__codigo = codigo
        self.__nome = nome
        self.__preco = preco

    # Getters: permitem consultar os atributos privados.
    def get_codigo(self):
        return self.__codigo

    def get_nome(self):
        return self.__nome

    def get_preco(self):
        return self.__preco

    # Setter com validação (R3).
    def set_preco(self, novo_preco):
        if novo_preco < 0:
            print("Erro: o preço não pode ser negativo.")
            return False

        self.__preco = novo_preco
        return True

    # Método abstrato: cada classe filha calcula de uma forma.
    @abstractmethod
    def calcular_preco(self):
        pass

    # Método normal que utiliza o método abstrato.
    def mostrar_preco_final(self):
        return self.calcular_preco()


# INTERFACE (R4): define uma ação promocional.
class Promocional(ABC):
    @abstractmethod
    def aplicar_desconto(self, percentual):
        pass


# CLASSE FILHA 1 (R2) E IMPLEMENTAÇÃO DA INTERFACE (R4).
class Lanche(ItemCardapio, Promocional):
    def __init__(self, codigo, nome, preco, adicional):
        super().__init__(codigo, nome, preco)
        self.__adicional = adicional

    def calcular_preco(self):
        # O preço do lanche inclui o valor do adicional.
        return self.get_preco() + self.__adicional

    def aplicar_desconto(self, percentual):
        if percentual < 0 or percentual > 100:
            print("Desconto inválido. Use um valor entre 0 e 100.")
            return self.calcular_preco()

        return self.calcular_preco() * (1 - percentual / 100)

    def __str__(self):
        return (f"[Lanche] Código: {self.get_codigo()} | "
                f"Nome: {self.get_nome()} | "
                f"Preço base: R$ {self.get_preco():.2f} | "
                f"Adicional: R$ {self.__adicional:.2f} | "
                f"Preço final: R$ {self.calcular_preco():.2f}")


# CLASSE FILHA 2 (R2) E IMPLEMENTAÇÃO DA INTERFACE (R4).
class Bebida(ItemCardapio, Promocional):
    def __init__(self, codigo, nome, preco, tamanho_ml):
        super().__init__(codigo, nome, preco)
        self.__tamanho_ml = tamanho_ml

    def calcular_preco(self):
        # Bebidas grandes recebem um acréscimo de tamanho.
        if self.__tamanho_ml >= 600:
            return self.get_preco() + 2.00
        return self.get_preco()

    def aplicar_desconto(self, percentual):
        if percentual < 0 or percentual > 100:
            print("Desconto inválido. Use um valor entre 0 e 100.")
            return self.calcular_preco()

        return self.calcular_preco() * (1 - percentual / 100)

    def __str__(self):
        return (f"[Bebida] Código: {self.get_codigo()} | "
                f"Nome: {self.get_nome()} | "
                f"Tamanho: {self.__tamanho_ml} ml | "
                f"Preço final: R$ {self.calcular_preco():.2f}")


# LISTA DE OBJETOS (R6). Começa com três itens cadastrados.
cardapio = [
    Lanche(1, "X-Burger", 18.00, 3.00),
    Lanche(2, "X-Salada", 20.00, 2.50),
    Bebida(3, "Refrigerante", 7.00, 600)
]


def encontrar_item(termo):
    """Procura um item pelo código ou pelo nome."""
    for item in cardapio:
        if str(item.get_codigo()) == termo:
            return item
        if item.get_nome().lower() == termo.lower():
            return item
    return None


def cadastrar_item():
    print("\n--- CADASTRAR ITEM ---")
    print("1 - Lanche")
    print("2 - Bebida")
    tipo = input("Escolha o tipo: ")

    if tipo not in ("1", "2"):
        print("Tipo inválido.")
        return

    try:
        codigo = int(input("Código: "))
        if any(item.get_codigo() == codigo for item in cardapio):
            print("Já existe um item com esse código.")
            return

        nome = input("Nome: ").strip()
        if not nome:
            print("O nome não pode ficar vazio.")
            return

        preco = float(input("Preço base (R$): ").replace(",", "."))
        if preco < 0:
            print("O preço não pode ser negativo.")
            return

        if tipo == "1":
            adicional = float(input("Valor do adicional (R$): ").replace(",", "."))
            if adicional < 0:
                print("O adicional não pode ser negativo.")
                return
            novo_item = Lanche(codigo, nome, preco, adicional)
        else:
            tamanho = int(input("Tamanho em ml: "))
            if tamanho <= 0:
                print("O tamanho deve ser maior que zero.")
                return
            novo_item = Bebida(codigo, nome, preco, tamanho)

        cardapio.append(novo_item)
        print("Item cadastrado com sucesso!")

    except ValueError:
        print("Entrada inválida. Digite números nos campos indicados.")


def listar_itens():
    print("\n--- CARDÁPIO ---")
    if not cardapio:
        print("O cardápio está vazio.")
        return

    for item in cardapio:
        # O print chama __str__() nos objetos.
        print(item)


def buscar_item():
    print("\n--- BUSCAR ITEM ---")
    termo = input("Digite o código ou o nome: ").strip()
    item = encontrar_item(termo)

    if item:
        print("Item encontrado:")
        print(item)
    else:
        print("Item não encontrado.")


def remover_item():
    print("\n--- REMOVER ITEM ---")
    termo = input("Digite o código ou o nome do item: ").strip()
    item = encontrar_item(termo)

    if item:
        cardapio.remove(item)
        print("Item removido com sucesso!")
    else:
        print("Item não encontrado.")


def executar_acao_sistema():
    print("\n--- PREÇOS CALCULADOS (POLIMORFISMO) ---")
    if not cardapio:
        print("Não há itens cadastrados.")
        return

    # POLIMORFISMO (R5): o mesmo método é chamado em objetos diferentes.
    for item in cardapio:
        print(f"{item.get_nome()}: R$ {item.mostrar_preco_final():.2f}")


def aplicar_promocao():
    print("\n--- APLICAR DESCONTO ---")
    termo = input("Digite o código ou o nome do item: ").strip()
    item = encontrar_item(termo)

    if item is None:
        print("Item não encontrado.")
        return

    percentual_texto = input("Percentual de desconto: ").replace(",", ".")
    try:
        percentual = float(percentual_texto)
        if not isinstance(item, Promocional):
            print("Este item não oferece desconto.")
            return

        novo_preco = item.aplicar_desconto(percentual)
        print(f"Preço com desconto: R$ {novo_preco:.2f}")
    except ValueError:
        print("Digite um percentual numérico.")


def testar_setter():
    print("\n--- TESTE DE ENCAPSULAMENTO ---")
    if not cardapio:
        print("Não há itens cadastrados para testar.")
        return

    item = cardapio[0]
    print(f"Item escolhido: {item.get_nome()}")
    print("Tentando definir preço negativo (-10)...")
    item.set_preco(-10)
    print(f"Preço atual continua: R$ {item.get_preco():.2f}")


def menu():
    while True:
        print("\n========== LANCHONETE ==========")
        print("1 - Cadastrar item")
        print("2 - Listar cardápio")
        print("3 - Buscar item")
        print("4 - Remover item")
        print("5 - Ação do sistema (calcular preços)")
        print("6 - Aplicar desconto")
        print("7 - Testar validação do preço")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_item()
        elif opcao == "2":
            listar_itens()
        elif opcao == "3":
            buscar_item()
        elif opcao == "4":
            remover_item()
        elif opcao == "5":
            executar_acao_sistema()
        elif opcao == "6":
            aplicar_promocao()
        elif opcao == "7":
            testar_setter()
        elif opcao == "0":
            print("Programa encerrado. Obrigado!")
            break
        else:
            print("Opção inválida. Escolha uma opção do menu.")


# Início do programa.
if __name__ == "__main__":
    menu()
