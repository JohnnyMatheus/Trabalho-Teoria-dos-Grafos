import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def criar_grafo():
    """Cria um grafo não direcionado com circuito euleriano ou caminho euleriano."""
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 6), 
                      (2, 6), (3, 4), (4, 5), (5, 6), (1, 5), (2, 3)])
    return G

def analisar_grafo(G):
    """Analisa as propriedades eulerianas do grafo."""
    graus = dict(G.degree())
    impares = [v for v, grau in graus.items() if grau % 2 != 0]
    conexo = nx.is_connected(G)

    print("\n--- Análise do Grafo ---")
    print("Graus dos vértices:", graus)
    print("Vértices com grau ímpar:", impares)
    print("Grafo conexo:", conexo)

    if not conexo:
        print("O grafo não é conexo, portanto não possui caminho ou circuito euleriano.")
        return False

    if len(impares) == 0:
        print("O grafo possui um circuito euleriano.")
        return "circuito"
    elif len(impares) == 2:
        print("O grafo possui um caminho euleriano.")
        return "caminho"
    else:
        print("O grafo não possui caminho ou circuito euleriano.")
        return False

def fleury(G_original, ax):
    """Implementação do algoritmo de Fleury com animação corrigida."""
    G = G_original.copy()
    graus = dict(G.degree())
    impares = [v for v, grau in graus.items() if grau % 2 != 0]

    if len(impares) > 2:
        print("O grafo não possui caminho/circuito euleriano.")
        return None

    inicio = impares[0] if impares else list(G.nodes())[0]
    caminho = [inicio]
    frames = []

    def update(frame):
        ax.clear()
        nx.draw(G_original, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', ax=ax)
        # Desenha todas as arestas percorridas até o frame atual
        for i in range(frame):
            if i + 1 < len(caminho):
                ax.add_artist(plt.Line2D(
                    [pos[caminho[i]][0], pos[caminho[i + 1]][0]], 
                    [pos[caminho[i]][1], pos[caminho[i + 1]][1]], 
                    color='red', linewidth=3, zorder=10
                ))
        ax.set_title(f"Fleury - Passo {frame}")
        return ax,

    while G.edges():
        vizinhos = list(G.neighbors(inicio))
        aresta_valida = False
        for vizinho in vizinhos:
            if G.number_of_edges(inicio, vizinho) == 0:
                continue  # Aresta já removida
            G_temp = G.copy()
            G_temp.remove_edge(inicio, vizinho)
            if nx.is_connected(G_temp) or len(G.edges()) == 1:
                G.remove_edge(inicio, vizinho)
                inicio = vizinho
                caminho.append(vizinho)
                aresta_valida = True
                frames.append(len(caminho) - 1)
                break
        if not aresta_valida:
            break  # Evita loops infinitos

    ani = animation.FuncAnimation(
        fig1, update, frames=range(len(caminho)), 
        interval=1000, repeat=False, blit=False
    )
    plt.show()
    return caminho

def hierholzer(G_original, ax):
    """Implementação do algoritmo de Hierholzer com animação."""
    G = G_original.copy()
    inicio = list(G.nodes())[0]
    ciclo = []

    def encontrar_ciclo(vertice):
        pilha = [vertice]
        ciclo_atual = []
        while pilha:
            v = pilha[-1]
            vizinhos = list(G.neighbors(v))
            if vizinhos:
                proximo = vizinhos[0]
                pilha.append(proximo)
                G.remove_edge(v, proximo)
            else:
                ciclo_atual.append(pilha.pop())
        return ciclo_atual

    ciclo = encontrar_ciclo(inicio)

    while any(G.edges()):
        for i, v in enumerate(ciclo):
            if list(G.neighbors(v)):
                novo_ciclo = encontrar_ciclo(v)
                ciclo = ciclo[:i] + novo_ciclo + ciclo[i+1:]
                break

    def update(frame):
        ax.clear()
        nx.draw(G_original, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', ax=ax)
        if frame < len(ciclo) - 1:
            ax.add_artist(plt.Line2D(
                [pos[ciclo[frame]][0], pos[ciclo[frame + 1]][0]], 
                [pos[ciclo[frame]][1], pos[ciclo[frame + 1]][1]], 
                color='green', linewidth=3, zorder=10
            ))
        ax.set_title(f"Hierholzer - Passo {frame}")
        return ax,

    ani = animation.FuncAnimation(
        fig2, update, frames=range(len(ciclo)), 
        interval=1000, repeat=False, blit=False
    )
    plt.show()
    return ciclo

# --- Execução principal ---
grafo = criar_grafo()
analisar_grafo(grafo)
pos = nx.spring_layout(grafo)  # Posições fixas para ambos os gráficos

# Gráfico 1: Fleury
fig1, ax1 = plt.subplots(figsize=(8, 6))
print("\n--- Algoritmo de Fleury ---")
caminho_fleury = fleury(grafo, ax1)
if caminho_fleury:
    print("Caminho Euleriano (Fleury):", caminho_fleury)

# Gráfico 2: Hierholzer (só abre após fechar o primeiro)
fig2, ax2 = plt.subplots(figsize=(8, 6))
print("\n--- Algoritmo de Hierholzer ---")
caminho_hierholzer = hierholzer(grafo, ax2)
print("Circuito Euleriano (Hierholzer):", caminho_hierholzer)
