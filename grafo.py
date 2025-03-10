# pip install networkx
# pip install matplotlib
# pip install scipy

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Função para exibir o menu
def exibir_menu():
    print("\n--- Menu ---")
    print("1. Mostrar ordem do grafo")
    print("2. Mostrar matriz de incidência")
    print("3. Calcular grau de um vértice")
    print("4. Calcular grau do grafo")
    print("5. Visualizar grafo")
    print("6. Sair")

# Função principal
def main():
    # Criando o grafo
    G = nx.Graph()

    # Adicionando vértices (cada letra do nome "Johnny Matheus")
    vertices = ['J', 'o', 'h', 'n', 'n', 'y', 'M', 'a', 't', 'h', 'e', 'u', 's']
    G.add_nodes_from(vertices)

    # Adicionando arestas para formar uma cadeia/caminho
    arestas = [('J', 'o'), ('o', 'h'), ('h', 'n'), ('n', 'n'), ('n', 'y'), ('y', 'M'), ('M', 'a'), ('a', 't'), ('t', 'h'), ('h', 'e'), ('e', 'u'), ('u', 's')]
    G.add_edges_from(arestas)

    # Adicionando uma aresta para formar um ciclo (conectando 's' de volta a 'J')
    G.add_edge('s', 'J')

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            # Ordem do Grafo (número de vértices)
            ordem_grafo = G.number_of_nodes()
            print("Ordem do Grafo:", ordem_grafo)

        elif opcao == '2':
            # Matriz de Incidência
            incidence_matrix = nx.incidence_matrix(G).toarray()
            print("Matriz de Incidência:\n", incidence_matrix)

        elif opcao == '3':
            # Grau de um Vértice
            vertice = input("Digite o vértice (letra): ")
            if vertice in G:
                grau = G.degree(vertice)
                print(f"Grau do vértice {vertice}: {grau}")
            else:
                print("Vértice não encontrado.")

        elif opcao == '4':
            # Grau do Grafo (maior grau entre os vértices)
            graus_vertices = dict(G.degree())
            grau_grafo = sum(graus_vertices.values()) * 2
            print("Grau do Grafo:", grau_grafo)

        elif opcao == '5':
            # Desenhando o grafo
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold')
            plt.title("Grafo do Nome 'Johnny Matheus'")
            plt.show()

        elif opcao == '6':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()