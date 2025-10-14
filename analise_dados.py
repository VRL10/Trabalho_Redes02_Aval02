import json
import matplotlib.pyplot as plt
import numpy as np

def gerar_graficos():
    # Carregar resultados
    with open('resultados_testes.json', 'r') as f:
        dados = json.load(f)
    
    # Gráfico de comparação de tempos
    servidores = list(dados.keys())
    medias_get = [dados[s]['estatisticas_get']['media'] for s in servidores]
    medias_post = [dados[s]['estatisticas_post']['media'] for s in servidores]
    
    x = np.arange(len(servidores))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, medias_get, width, label='GET', alpha=0.8)
    bars2 = ax.bar(x + width/2, medias_post, width, label='POST', alpha=0.8)
    
    ax.set_xlabel('Tipo de Servidor')
    ax.set_ylabel('Tempo Médio (segundos)')
    ax.set_title('Comparação de Performance: Sequencial vs Concorrente')
    ax.set_xticks(x)
    ax.set_xticklabels(servidores)
    ax.legend()
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('comparacao_performance.png')
    plt.show()
    
    print("Gráfico salvo como 'comparacao_performance.png'")

if __name__ == "__main__":
    gerar_graficos()