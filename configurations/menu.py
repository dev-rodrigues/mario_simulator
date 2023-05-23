import pygame

from domain.entities.game import Game
from domain.entities.mario import Mario
from service.training import train


def show_menu():
    print("1 - Start Training")
    print("2 - Start Server")
    print("3 - Running with genome")
    print("4 - Exit")


def start_training():
    if not exist_genome_on_file():
        mario = train()
        write_genome_on_file(mario)
    else:
        print("Genome already exists.")
        print("Do you want to use the existing genome?")
        print("1 - Yes")
        print("2 - No")
        choice = input("Select an option")
        if choice == '1':
            mario = train()
            delete_genome_on_file()
            write_genome_on_file(mario)

    print("Concluded training.")


def running_with_genome():
    if exist_genome_on_file():
        genome, genomeOutput = read_genome_on_file()
        mario = Mario(genome, genomeOutput)
        game = Game(mario)
        game.run()
        pygame.quit()
        print("Fitness:", mario.fitness)

    else:
        print("Genome not found.")


def read_genome_on_file():
    file = open("genome.txt", "r")
    genome_lines = file.readlines()

    genome = [float(line.strip()) for line in genome_lines[:-1]]

    genome_output = [float(genome_lines[-1].strip()[1:-2])]  # Remove os colchetes

    file.close()
    return genome, genome_output


def write_genome_on_file(mario):
    file = open("genome.txt", "w")

    for gene in mario.genome:
        file.write(str(gene) + "\n")

    file.write(str(mario.genomeOutput))

    file.close()


def delete_genome_on_file():
    file = open("genome.txt", "w")
    file.write("")
    file.close()


def exist_genome_on_file():
    try:
        file = open("genome.txt", "r")
        file.close()
        return True
    except IOError:
        return False


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
            running_with_genome()

        elif choice == '3':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")
