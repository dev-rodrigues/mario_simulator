from service.training import train


def show_menu():
    print("1 - Start Training")
    print("2 - Start Server")
    print("3 - Exit")


def start_training():
    train()


def start_server():
    print("Iniciando servidor...")


def menu():
    while True:
        show_menu()
        choice = input("Selecione uma opção: ")

        if choice == '1':
            start_training()
        elif choice == '2':
            start_server()
        elif choice == '3':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
