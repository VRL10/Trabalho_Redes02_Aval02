import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import os
import pandas as pd
from scipy import stats

# Criar diretório para salvar as imagens
os.makedirs('graficos_relatorio', exist_ok=True)

# Carregar dados do JSON
with open('resultados/metricas_completas.json', 'r') as f:
    dados = json.load(f)

# Configuração global de estilo
plt.style.use('default')
sns.set_palette("husl")

print("Gerando gráficos individuais para o relatório...")

# Definir cenários e títulos
cenarios = ['carga_baixa', 'carga_media', 'carga_alta']
titulos = ['Carga Baixa (10 req)', 'Carga Média (20 req)', 'Carga Alta (30 req)']
cores = ['#2E86AB', '#A23B72']

# =============================================================================
# 1. COMPARAÇÃO DE THROUGHPUT POR CENÁRIO (3 IMAGENS SEPARADAS)
# =============================================================================
print("Gerando gráficos 1-3: Comparação de Throughput por Cenário")

for i, cenario in enumerate(cenarios):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calcular médias
    seq_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['sequencial']]
    conc_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['concorrente']]
    
    mean_seq = np.mean(seq_throughputs)
    mean_conc = np.mean(conc_throughputs)
    
    # Gráfico de barras
    bars = ax.bar(['Sequencial', 'Concorrente'], [mean_seq, mean_conc], 
                  color=cores, alpha=0.8)
    
    ax.set_title(f'Throughput - {titulos[i]}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Throughput (req/s)')
    ax.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'graficos_relatorio/throughput_{cenario}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico {i+1} salvo: throughput_{cenario}.png")

# =============================================================================
# 4. TEMPO MÉDIO DE RESPOSTA POR CENÁRIO (3 IMAGENS SEPARADAS)
# =============================================================================
print("Gerando gráficos 4-6: Tempo Médio de Resposta por Cenário")

for i, cenario in enumerate(cenarios):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    seq_tempos = [run['tempo_medio'] * 1000 for run in dados['cenarios'][cenario]['sequencial']]
    conc_tempos = [run['tempo_medio'] * 1000 for run in dados['cenarios'][cenario]['concorrente']]
    
    mean_seq = np.mean(seq_tempos)
    mean_conc = np.mean(conc_tempos)
    
    bars = ax.bar(['Sequencial', 'Concorrente'], [mean_seq, mean_conc], 
                  color=cores, alpha=0.8)
    
    ax.set_title(f'Tempo Médio de Resposta - {titulos[i]}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Tempo Médio (ms)')
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}ms', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'graficos_relatorio/tempo_medio_{cenario}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico {i+4} salvo: tempo_medio_{cenario}.png")

# =============================================================================
# 7. EVOLUÇÃO DO THROUGHPUT (3 IMAGENS SEPARADAS)
# =============================================================================
print("Gerando gráficos 7-9: Evolução do Throughput por Cenário")

for i, cenario in enumerate(cenarios):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    execucoes = range(1, 11)
    
    seq_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['sequencial']]
    conc_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['concorrente']]
    
    ax.plot(execucoes, seq_throughputs, marker='o', linewidth=2, 
            label='Sequencial', color=cores[0])
    ax.plot(execucoes, conc_throughputs, marker='s', linewidth=2, 
            label='Concorrente', color=cores[1])
    
    ax.set_title(f'Evolução do Throughput - {titulos[i]}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Número da Execução')
    ax.set_ylabel('Throughput (req/s)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xticks(execucoes)

    plt.tight_layout()
    plt.savefig(f'graficos_relatorio/evolucao_throughput_{cenario}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico {i+7} salvo: evolucao_throughput_{cenario}.png")

# =============================================================================
# 10. BOXPLOT - DISTRIBUIÇÃO DO THROUGHPUT (3 IMAGENS SEPARADAS)
# =============================================================================
print("Gerando gráficos 10-12: Boxplot de Throughput por Cenário")

for i, cenario in enumerate(cenarios):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    seq_data = [run['throughput'] for run in dados['cenarios'][cenario]['sequencial']]
    conc_data = [run['throughput'] for run in dados['cenarios'][cenario]['concorrente']]
    
    boxplots = ax.boxplot([seq_data, conc_data], 
                          labels=['Sequencial', 'Concorrente'],
                          patch_artist=True)
    
    # Cores
    for patch, color in zip(boxplots['boxes'], cores):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_title(f'Distribuição do Throughput - {titulos[i]}', fontsize=14, fontweight='bold')
    ax.set_ylabel('Throughput (req/s)')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'graficos_relatorio/boxplot_throughput_{cenario}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico {i+10} salvo: boxplot_throughput_{cenario}.png")

# =============================================================================
# 13. TAXA DE SUCESSO (1 IMAGEM)
# =============================================================================
print("Gerando gráfico 13: Taxa de Sucesso")

fig, ax = plt.subplots(figsize=(12, 6))

categorias = []
valores = []

for cenario in cenarios:
    seq_sucesso = np.mean([run['taxa_sucesso'] for run in dados['cenarios'][cenario]['sequencial']])
    conc_sucesso = np.mean([run['taxa_sucesso'] for run in dados['cenarios'][cenario]['concorrente']])
    
    categorias.extend([f'{cenario.replace("_", " ").title()}\nSequencial', 
                      f'{cenario.replace("_", " ").title()}\nConcorrente'])
    valores.extend([seq_sucesso, conc_sucesso])

bars = ax.bar(categorias, valores, color=cores * 3, alpha=0.8)
ax.set_ylabel('Taxa de Sucesso (%)')
ax.set_title('Taxa de Sucesso por Cenário e Tipo de Servidor', fontsize=14, fontweight='bold')
ax.set_ylim(90, 105)
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('graficos_relatorio/taxa_sucesso.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 13 salvo: taxa_sucesso.png")

# =============================================================================
# 14. ANÁLISE DE DESEMPENHO RELATIVO (1 IMAGEM)
# =============================================================================
print("Gerando gráfico 14: Desempenho Relativo")

# Calcular vantagem do concorrente em cada cenário
vantagens = []
for cenario in cenarios:
    seq_throughput = np.mean([run['throughput'] for run in dados['cenarios'][cenario]['sequencial']])
    conc_throughput = np.mean([run['throughput'] for run in dados['cenarios'][cenario]['concorrente']])
    
    vantagem = (conc_throughput / seq_throughput) * 100
    vantagens.append(vantagem)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(titulos, vantagens, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)

ax.set_ylabel('Desempenho Relativo (%)')
ax.set_title('Vantagem/Desvantagem do Servidor Concorrente\n(100% = Igual desempenho)', 
             fontsize=14, fontweight='bold')
ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='Igual desempenho')
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

ax.legend()
plt.tight_layout()
plt.savefig('graficos_relatorio/desempenho_relativo.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 14 salvo: desempenho_relativo.png")

# =============================================================================
# 15. RESUMO ESTATÍSTICO (1 IMAGEM)
# =============================================================================
print("Gerando gráfico 15: Resumo Estatístico")

# Preparar dados para tabela
dados_resumo = []
for cenario in cenarios:
    seq_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['sequencial']]
    conc_throughputs = [run['throughput'] for run in dados['cenarios'][cenario]['concorrente']]
    
    dados_resumo.append({
        'Cenário': cenario.replace('_', ' ').title(),
        'Seq_Media': np.mean(seq_throughputs),
        'Seq_Desvio': np.std(seq_throughputs),
        'Conc_Media': np.mean(conc_throughputs),
        'Conc_Desvio': np.std(conc_throughputs),
        'Vantagem_%': (np.mean(conc_throughputs) / np.mean(seq_throughputs)) * 100
    })

# Criar tabela visual
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('tight')
ax.axis('off')

tabela_data = []
for resumo in dados_resumo:
    tabela_data.append([
        resumo['Cenário'],
        f"{resumo['Seq_Media']:.1f} ± {resumo['Seq_Desvio']:.1f}",
        f"{resumo['Conc_Media']:.1f} ± {resumo['Conc_Desvio']:.1f}",
        f"{resumo['Vantagem_%']:.1f}%"
    ])

tabela = ax.table(cellText=tabela_data,
                 colLabels=['Cenário', 'Sequencial (req/s)', 'Concorrente (req/s)', 'Vantagem Relativa'],
                 cellLoc='center',
                 loc='center')

tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1, 1.5)

plt.title('Resumo Estatístico - Comparação de Desempenho', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('graficos_relatorio/resumo_estatistico.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 15 salvo: resumo_estatistico.png")

print(f"\n TODOS OS 15 GRÁFICOS FORAM GERADOS COM SUCESSO!")
print(f" Pasta: graficos_relatorio/")
print(f" Gráficos criados:")
print(f"   1-3.  throughput_carga_baixa.png, throughput_carga_media.png, throughput_carga_alta.png")
print(f"   4-6.  tempo_medio_carga_baixa.png, tempo_medio_carga_media.png, tempo_medio_carga_alta.png")
print(f"   7-9.  evolucao_throughput_carga_baixa.png, evolucao_throughput_carga_media.png, evolucao_throughput_carga_alta.png")
print(f"   10-12.boxplot_throughput_carga_baixa.png, boxplot_throughput_carga_media.png, boxplot_throughput_carga_alta.png")
print(f"   13.   taxa_sucesso.png")
print(f"   14.   desempenho_relativo.png")
print(f"   15.   resumo_estatistico.png")