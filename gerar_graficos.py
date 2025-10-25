import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
import os
import pandas as pd

# Criar diretório para salvar as imagens se não existir
os.makedirs('graficos', exist_ok=True)

# Carregar dados do JSON
with open('resultados/metricas_completas.json', 'r') as f:
    dados = json.load(f)

# Configuração global de estilo
plt.style.use('default')
sns.set_palette("husl")

print("Gerando gráficos...")

# =============================================================================
# 1. TEMPO DE RESPOSTA - SERVIDOR SEQUENCIAL
# =============================================================================
print("Gerando gráfico 1: Tempo de Resposta - Servidor Sequencial")

# Extrair dados para Servidor Sequencial
seq_get_tempos = [teste['tempo_medio'] * 1000 for teste in dados['servidor_sequencial']['testes_get_sequenciais']]
seq_post_tempos = [teste['tempo_medio'] * 1000 for teste in dados['servidor_sequencial']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Criar boxplots
boxplots = ax.boxplot([seq_get_tempos, seq_post_tempos], 
                     labels=['GET Sequencial', 'POST Sequencial'],
                     patch_artist=True,
                     widths=0.6)

# Cores para os boxplots
cores = ['#2E86AB', '#A23B72']
for patch, color in zip(boxplots['boxes'], cores):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Melhorar aparência
ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12)
ax.set_title('Tempo de Resposta - Servidor Sequencial', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/tempo_resposta_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()  # Fechar a figura para liberar memória
print("✓ Gráfico 1 salvo: graficos/tempo_resposta_sequencial.png")

# =============================================================================
# 2. TEMPO DE RESPOSTA - SERVIDOR CONCORRENTE
# =============================================================================
print("Gerando gráfico 2: Tempo de Resposta - Servidor Concorrente")

# Extrair dados para Servidor Concorrente
conc_get_tempos = [teste['tempo_medio'] * 1000 for teste in dados['servidor_concorrente']['testes_get_sequenciais']]
conc_post_tempos = [teste['tempo_medio'] * 1000 for teste in dados['servidor_concorrente']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Criar boxplots
boxplots = ax.boxplot([conc_get_tempos, conc_post_tempos], 
                     labels=['GET Concorrente', 'POST Concorrente'],
                     patch_artist=True,
                     widths=0.6)

# Cores para os boxplots
cores = ['#2E86AB', '#A23B72']
for patch, color in zip(boxplots['boxes'], cores):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Melhorar aparência
ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12)
ax.set_title('Tempo de Resposta - Servidor Concorrente', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/tempo_resposta_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 2 salvo: graficos/tempo_resposta_concorrente.png")

# =============================================================================
# 3. THROUGHPUT - SERVIDOR SEQUENCIAL
# =============================================================================
print("Gerando gráfico 3: Throughput - Servidor Sequencial")

# Extrair dados de throughput para Servidor Sequencial
seq_get_throughput = [teste['throughput'] for teste in dados['servidor_sequencial']['testes_get_sequenciais']]
seq_post_throughput = [teste['throughput'] for teste in dados['servidor_sequencial']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Dados para o gráfico de barras
categorias = ['GET Sequencial', 'POST Sequencial']
medias = [np.mean(seq_get_throughput), np.mean(seq_post_throughput)]
desvios = [np.std(seq_get_throughput), np.std(seq_post_throughput)]

# Criar barras - SEM TRAÇOS (sem error bars)
barras = ax.bar(categorias, medias, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.7)

# Adicionar valores nas barras
for i, barra in enumerate(barras):
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2., altura + 5,
            f'{altura:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Melhorar aparência
ax.set_ylabel('Throughput (req/s)', fontsize=12)
ax.set_title('Throughput - Servidor Sequencial', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/throughput_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 3 salvo: graficos/throughput_sequencial.png")

# =============================================================================
# 4. THROUGHPUT - SERVIDOR CONCORRENTE
# =============================================================================
print("Gerando gráfico 4: Throughput - Servidor Concorrente")

# Extrair dados de throughput para Servidor Concorrente
conc_get_throughput = [teste['throughput'] for teste in dados['servidor_concorrente']['testes_get_sequenciais']]
conc_post_throughput = [teste['throughput'] for teste in dados['servidor_concorrente']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Dados para o gráfico de barras
categorias = ['GET Concorrente', 'POST Concorrente']
medias = [np.mean(conc_get_throughput), np.mean(conc_post_throughput)]
desvios = [np.std(conc_get_throughput), np.std(conc_post_throughput)]

# Criar barras - SEM TRAÇOS (sem error bars)
barras = ax.bar(categorias, medias, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.7)

# Adicionar valores nas barras
for i, barra in enumerate(barras):
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2., altura + 0.5,
            f'{altura:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Melhorar aparência
ax.set_ylabel('Throughput (req/s)', fontsize=12)
ax.set_title('Throughput - Servidor Concorrente', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/throughput_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 4 salvo: graficos/throughput_concorrente.png")

# =============================================================================
# 5. TAXA DE SUCESSO - SERVIDOR SEQUENCIAL
# =============================================================================
print("Gerando gráfico 5: Taxa de Sucesso - Servidor Sequencial")

# Extrair dados de taxa de sucesso para Servidor Sequencial
seq_get_sucesso = [teste['taxa_sucesso'] for teste in dados['servidor_sequencial']['testes_get_sequenciais']]
seq_post_sucesso = [teste['taxa_sucesso'] for teste in dados['servidor_sequencial']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Dados para o gráfico de barras
categorias = ['GET Sequencial', 'POST Sequencial']
medias = [np.mean(seq_get_sucesso), np.mean(seq_post_sucesso)]

# Criar barras
barras = ax.bar(categorias, medias, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.7)

# Adicionar valores nas barras
for i, barra in enumerate(barras):
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2., altura + 0.5,
            f'{altura:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Melhorar aparência
ax.set_ylabel('Taxa de Sucesso (%)', fontsize=12)
ax.set_title('Taxa de Sucesso - Servidor Sequencial', fontsize=14, fontweight='bold')
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)


plt.tight_layout()
plt.savefig('graficos/taxa_sucesso_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 5 salvo: graficos/taxa_sucesso_sequencial.png")

# =============================================================================
# 6. TAXA DE SUCESSO - SERVIDOR CONCORRENTE
# =============================================================================
print("Gerando gráfico 6: Taxa de Sucesso - Servidor Concorrente")

# Extrair dados de taxa de sucesso para Servidor Concorrente
conc_get_sucesso = [teste['taxa_sucesso'] for teste in dados['servidor_concorrente']['testes_get_sequenciais']]
conc_post_sucesso = [teste['taxa_sucesso'] for teste in dados['servidor_concorrente']['testes_post_sequenciais']]

fig, ax = plt.subplots(figsize=(10, 6))

# Dados para o gráfico de barras
categorias = ['GET Concorrente', 'POST Concorrente']
medias = [np.mean(conc_get_sucesso), np.mean(conc_post_sucesso)]

# Criar barras
barras = ax.bar(categorias, medias, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.7)

# Adicionar valores nas barras
for i, barra in enumerate(barras):
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2., altura + 0.5,
            f'{altura:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Melhorar aparência
ax.set_ylabel('Taxa de Sucesso (%)', fontsize=12)
ax.set_title('Taxa de Sucesso - Servidor Concorrente', fontsize=14, fontweight='bold')
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)


plt.tight_layout()
plt.savefig('graficos/taxa_sucesso_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
# =============================================================================
# 7. COMPARAÇÃO DIRETA: THROUGHPUT SEQUENCIAL vs CONCORRENTE - GET
# =============================================================================
print("Gerando gráfico 7: Comparação Throughput - GET")

fig, ax = plt.subplots(figsize=(10, 6))

seq_get_throughput = np.mean([t['throughput'] for t in dados['servidor_sequencial']['testes_get_sequenciais']])
conc_get_throughput = np.mean([t['throughput'] for t in dados['servidor_concorrente']['testes_get_sequenciais']])

categorias = ['Sequencial', 'Concorrente']
valores = [seq_get_throughput, conc_get_throughput]

bars = ax.bar(categorias, valores, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.6)

ax.set_ylabel('Throughput (req/s)')
ax.set_title('Comparação de Throughput - GET\nSequencial vs Concorrente', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 10,
            f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('graficos/comparacao_throughput_get.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 7 salvo: graficos/comparacao_throughput_get.png")

# =============================================================================
# 8. COMPARAÇÃO DIRETA: THROUGHPUT SEQUENCIAL vs CONCORRENTE - POST
# =============================================================================
print("Gerando gráfico 8: Comparação Throughput - POST")

fig, ax = plt.subplots(figsize=(10, 6))

seq_post_throughput = np.mean([t['throughput'] for t in dados['servidor_sequencial']['testes_post_sequenciais']])
conc_post_throughput = np.mean([t['throughput'] for t in dados['servidor_concorrente']['testes_post_sequenciais']])

categorias = ['Sequencial', 'Concorrente']
valores = [seq_post_throughput, conc_post_throughput]

bars = ax.bar(categorias, valores, color=['#2E86AB', '#A23B72'], alpha=0.8, width=0.6)

ax.set_ylabel('Throughput (req/s)')
ax.set_title('Comparação de Throughput - POST\nSequencial vs Concorrente', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('graficos/comparacao_throughput_post.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 8 salvo: graficos/comparacao_throughput_post.png")

# =============================================================================
# 9. EVOLUÇÃO DO THROUGHPUT - SEQUENCIAL GET
# =============================================================================
print("Gerando gráfico 9: Evolução Throughput - Sequencial GET")

fig, ax = plt.subplots(figsize=(10, 6))

execucoes = range(1, 11)
ax.plot(execucoes, [t['throughput'] for t in dados['servidor_sequencial']['testes_get_sequenciais']], 
        marker='o', linewidth=2, color='#2E86AB')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Throughput (req/s)')
ax.set_title('Evolução do Throughput - GET Sequencial', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/evolucao_throughput_get_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 9 salvo: graficos/evolucao_throughput_get_sequencial.png")

# =============================================================================
# 10. EVOLUÇÃO DO THROUGHPUT - SEQUENCIAL POST
# =============================================================================
print("Gerando gráfico 10: Evolução Throughput - Sequencial POST")

fig, ax = plt.subplots(figsize=(10, 6))

execucoes = range(1, 11)
ax.plot(execucoes, [t['throughput'] for t in dados['servidor_sequencial']['testes_post_sequenciais']], 
        marker='s', linewidth=2, color='#A23B72')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Throughput (req/s)')
ax.set_title('Evolução do Throughput - POST Sequencial', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/evolucao_throughput_post_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 10 salvo: graficos/evolucao_throughput_post_sequencial.png")

# =============================================================================
# 11. EVOLUÇÃO DO THROUGHPUT - CONCORRENTE GET
# =============================================================================
print("Gerando gráfico 11: Evolução Throughput - Concorrente GET")

fig, ax = plt.subplots(figsize=(10, 6))

execucoes = range(1, 11)
ax.plot(execucoes, [t['throughput'] for t in dados['servidor_concorrente']['testes_get_sequenciais']], 
        marker='o', linewidth=2, color='#2E86AB')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Throughput (req/s)')
ax.set_title('Evolução do Throughput - GET Concorrente', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/evolucao_throughput_get_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 11 salvo: graficos/evolucao_throughput_get_concorrente.png")

# =============================================================================
# 12. EVOLUÇÃO DO THROUGHPUT - CONCORRENTE POST
# =============================================================================
print("Gerando gráfico 12: Evolução Throughput - Concorrente POST")

fig, ax = plt.subplots(figsize=(10, 6))

execucoes = range(1, 11)
ax.plot(execucoes, [t['throughput'] for t in dados['servidor_concorrente']['testes_post_sequenciais']], 
        marker='s', linewidth=2, color='#A23B72')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Throughput (req/s)')
ax.set_title('Evolução do Throughput - POST Concorrente', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/evolucao_throughput_post_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 12 salvo: graficos/evolucao_throughput_post_concorrente.png")

# =============================================================================
# 13. DISTRIBUIÇÃO DE LATÊNCIA - GET SEQUENCIAL
# =============================================================================
print("Gerando gráfico 13: Distribuição Latência - GET Sequencial")

fig, ax = plt.subplots(figsize=(10, 6))

seq_get_tempos = [t['tempo_medio'] * 1000 for t in dados['servidor_sequencial']['testes_get_sequenciais']]

ax.hist(seq_get_tempos, bins=8, alpha=0.7, color='#2E86AB', edgecolor='black')
ax.set_xlabel('Tempo de Resposta (ms)')
ax.set_ylabel('Frequência')
ax.set_title('Distribuição de Latência - GET Sequencial', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/distribuicao_latencia_get_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 13 salvo: graficos/distribuicao_latencia_get_sequencial.png")

# =============================================================================
# 14. DISTRIBUIÇÃO DE LATÊNCIA - POST SEQUENCIAL
# =============================================================================
print("Gerando gráfico 14: Distribuição Latência - POST Sequencial")

fig, ax = plt.subplots(figsize=(10, 6))

seq_post_tempos = [t['tempo_medio'] * 1000 for t in dados['servidor_sequencial']['testes_post_sequenciais']]

ax.hist(seq_post_tempos, bins=8, alpha=0.7, color='#A23B72', edgecolor='black')
ax.set_xlabel('Tempo de Resposta (ms)')
ax.set_ylabel('Frequência')
ax.set_title('Distribuição de Latência - POST Sequencial', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/distribuicao_latencia_post_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 14 salvo: graficos/distribuicao_latencia_post_sequencial.png")

# =============================================================================
# 15. DISTRIBUIÇÃO DE LATÊNCIA - GET CONCORRENTE
# =============================================================================
print("Gerando gráfico 15: Distribuição Latência - GET Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

conc_get_tempos = [t['tempo_medio'] * 1000 for t in dados['servidor_concorrente']['testes_get_sequenciais']]

ax.hist(conc_get_tempos, bins=8, alpha=0.7, color='#2E86AB', edgecolor='black')
ax.set_xlabel('Tempo de Resposta (ms)')
ax.set_ylabel('Frequência')
ax.set_title('Distribuição de Latência - GET Concorrente', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/distribuicao_latencia_get_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 15 salvo: graficos/distribuicao_latencia_get_concorrente.png")

# =============================================================================
# 16. DISTRIBUIÇÃO DE LATÊNCIA - POST CONCORRENTE
# =============================================================================
print("Gerando gráfico 16: Distribuição Latência - POST Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

conc_post_tempos = [t['tempo_medio'] * 1000 for t in dados['servidor_concorrente']['testes_post_sequenciais']]

ax.hist(conc_post_tempos, bins=8, alpha=0.7, color='#A23B72', edgecolor='black')
ax.set_xlabel('Tempo de Resposta (ms)')
ax.set_ylabel('Frequência')
ax.set_title('Distribuição de Latência - POST Concorrente', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('graficos/distribuicao_latencia_post_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 16 salvo: graficos/distribuicao_latencia_post_concorrente.png")

# =============================================================================
# 17. ANÁLISE DE FALHAS - GET CONCORRENTE
# =============================================================================
print("Gerando gráfico 17: Análise de Falhas - GET Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

conc_get_falhas = [50 - t['sucessos'] for t in dados['servidor_sequencial']['testes_get_concorrentes']]
conc_get_sucessos = [t['sucessos'] for t in dados['servidor_sequencial']['testes_get_concorrentes']]

execucoes = range(1, 11)
ax.bar(execucoes, conc_get_sucessos, color='#2E86AB', alpha=0.7, label='Sucessos')
ax.bar(execucoes, conc_get_falhas, bottom=conc_get_sucessos, color='#FF6B6B', alpha=0.7, label='Falhas')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Número de Requisições')
ax.set_title('Análise de Sucessos e Falhas - GET Concorrente', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/analise_falhas_get_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 17 salvo: graficos/analise_falhas_get_concorrente.png")

# =============================================================================
# 18. ANÁLISE DE FALHAS - POST CONCORRENTE
# =============================================================================
print("Gerando gráfico 18: Análise de Falhas - POST Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

conc_post_falhas = [50 - t['sucessos'] for t in dados['servidor_sequencial']['testes_post_concorrentes']]
conc_post_sucessos = [t['sucessos'] for t in dados['servidor_sequencial']['testes_post_concorrentes']]

execucoes = range(1, 11)
ax.bar(execucoes, conc_post_sucessos, color='#A23B72', alpha=0.7, label='Sucessos')
ax.bar(execucoes, conc_post_falhas, bottom=conc_post_sucessos, color='#FF6B6B', alpha=0.7, label='Falhas')

ax.set_xlabel('Número da Execução')
ax.set_ylabel('Número de Requisições')
ax.set_title('Análise de Sucessos e Falhas - POST Concorrente', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xticks(execucoes)

plt.tight_layout()
plt.savefig('graficos/analise_falhas_post_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 18 salvo: graficos/analise_falhas_post_concorrente.png")

# =============================================================================
# 19. RAZÃO GET/POST - SEQUENCIAL
# =============================================================================
print("Gerando gráfico 19: Razão GET/POST - Sequencial")

fig, ax = plt.subplots(figsize=(10, 6))

seq_get_throughput = np.mean([t['throughput'] for t in dados['servidor_sequencial']['testes_get_sequenciais']])
seq_post_throughput = np.mean([t['throughput'] for t in dados['servidor_sequencial']['testes_post_sequenciais']])
seq_ratio = seq_get_throughput / seq_post_throughput

ax.bar(['Sequencial'], [seq_ratio], color='#4ECDC4', alpha=0.8, width=0.6)
ax.set_ylabel('Razão GET/POST')
ax.set_title('Razão de Performance: GET vs POST\nServidor Sequencial', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Linha de referência (1:1)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Igual performance')

ax.text(0, seq_ratio + 0.1, f'{seq_ratio:.1f}x', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.legend()

plt.tight_layout()
plt.savefig('graficos/razao_get_post_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 19 salvo: graficos/razao_get_post_sequencial.png")

# =============================================================================
# 20. RAZÃO GET/POST - CONCORRENTE
# =============================================================================
print("Gerando gráfico 20: Razão GET/POST - Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

conc_get_throughput = np.mean([t['throughput'] for t in dados['servidor_concorrente']['testes_get_sequenciais']])
conc_post_throughput = np.mean([t['throughput'] for t in dados['servidor_concorrente']['testes_post_sequenciais']])
conc_ratio = conc_get_throughput / conc_post_throughput

ax.bar(['Concorrente'], [conc_ratio], color='#45B7D1', alpha=0.8, width=0.6)
ax.set_ylabel('Razão GET/POST')
ax.set_title('Razão de Performance: GET vs POST\nServidor Concorrente', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Linha de referência (1:1)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Igual performance')

ax.text(0, conc_ratio + 0.1, f'{conc_ratio:.1f}x', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.legend()

plt.tight_layout()
plt.savefig('graficos/razao_get_post_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 20 salvo: graficos/razao_get_post_concorrente.png")

# =============================================================================
# 21. CONSISTÊNCIA - SEQUENCIAL
# =============================================================================
print("Gerando gráfico 21: Consistência - Sequencial")

fig, ax = plt.subplots(figsize=(10, 6))

# Coeficiente de variação (desvio padrão / média)
def coef_variacao(dados):
    return (np.std(dados) / np.mean(dados)) * 100

cv_seq_get = coef_variacao([t['throughput'] for t in dados['servidor_sequencial']['testes_get_sequenciais']])
cv_seq_post = coef_variacao([t['throughput'] for t in dados['servidor_sequencial']['testes_post_sequenciais']])

categorias = ['GET Sequencial', 'POST Sequencial']
cv_values = [cv_seq_get, cv_seq_post]

bars = ax.bar(categorias, cv_values, color=['#2E86AB', '#A23B72'], alpha=0.7)
ax.set_ylabel('Coeficiente de Variação (%)')
ax.set_title('Consistência do Desempenho - Servidor Sequencial\n(Menor = Mais Consistente)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('graficos/consistencia_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 21 salvo: graficos/consistencia_sequencial.png")

# =============================================================================
# 22. CONSISTÊNCIA - CONCORRENTE
# =============================================================================
print("Gerando gráfico 22: Consistência - Concorrente")

fig, ax = plt.subplots(figsize=(10, 6))

cv_conc_get = coef_variacao([t['throughput'] for t in dados['servidor_concorrente']['testes_get_sequenciais']])
cv_conc_post = coef_variacao([t['throughput'] for t in dados['servidor_concorrente']['testes_post_sequenciais']])

categorias = ['GET Concorrente', 'POST Concorrente']
cv_values = [cv_conc_get, cv_conc_post]

bars = ax.bar(categorias, cv_values, color=['#2E86AB', '#A23B72'], alpha=0.7)
ax.set_ylabel('Coeficiente de Variação (%)')
ax.set_title('Consistência do Desempenho - Servidor Concorrente\n(Menor = Mais Consistente)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('graficos/consistencia_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 22 salvo: graficos/consistencia_concorrente.png")

# =============================================================================
# 23. HEATMAP DE CORRELAÇÃO - SEQUENCIAL
# =============================================================================
print("Gerando gráfico 23: Heatmap Correlação - Sequencial")

fig, ax = plt.subplots(figsize=(8, 6))

# Preparar dados para correlação - apenas sequencial
dados_corr_seq = []
for teste in dados['servidor_sequencial']['testes_get_sequenciais'] + \
               dados['servidor_sequencial']['testes_post_sequenciais']:
    dados_corr_seq.append({
        'throughput': teste['throughput'],
        'tempo_medio': teste['tempo_medio'] * 1000,
        'taxa_sucesso': teste['taxa_sucesso'],
        'desvio_padrao': teste['desvio_padrao'] * 1000
    })

df_seq = pd.DataFrame(dados_corr_seq)
correlation_matrix_seq = df_seq.corr()

im = ax.imshow(correlation_matrix_seq, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

# Adicionar valores nas células
for i in range(len(correlation_matrix_seq.columns)):
    for j in range(len(correlation_matrix_seq.columns)):
        text = ax.text(j, i, f'{correlation_matrix_seq.iloc[i, j]:.2f}',
                       ha="center", va="center", color="white" if abs(correlation_matrix_seq.iloc[i, j]) > 0.5 else "black",
                       fontweight='bold')

ax.set_xticks(range(len(correlation_matrix_seq.columns)))
ax.set_yticks(range(len(correlation_matrix_seq.columns)))
ax.set_xticklabels(correlation_matrix_seq.columns, rotation=45)
ax.set_yticklabels(correlation_matrix_seq.columns)
ax.set_title('Matriz de Correlação - Servidor Sequencial', fontsize=14, fontweight='bold')

# Barra de cores
cbar = plt.colorbar(im)
cbar.set_label('Correlação', rotation=270, labelpad=15)

plt.tight_layout()
plt.savefig('graficos/heatmap_correlacao_sequencial.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 23 salvo: graficos/heatmap_correlacao_sequencial.png")

# =============================================================================
# 24. HEATMAP DE CORRELAÇÃO - CONCORRENTE
# =============================================================================
print("Gerando gráfico 24: Heatmap Correlação - Concorrente")

fig, ax = plt.subplots(figsize=(8, 6))

# Preparar dados para correlação - apenas concorrente
dados_corr_conc = []
for teste in dados['servidor_concorrente']['testes_get_sequenciais'] + \
               dados['servidor_concorrente']['testes_post_sequenciais']:
    dados_corr_conc.append({
        'throughput': teste['throughput'],
        'tempo_medio': teste['tempo_medio'] * 1000,
        'taxa_sucesso': teste['taxa_sucesso'],
        'desvio_padrao': teste['desvio_padrao'] * 1000
    })

df_conc = pd.DataFrame(dados_corr_conc)
correlation_matrix_conc = df_conc.corr()

im = ax.imshow(correlation_matrix_conc, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

# Adicionar valores nas células
for i in range(len(correlation_matrix_conc.columns)):
    for j in range(len(correlation_matrix_conc.columns)):
        text = ax.text(j, i, f'{correlation_matrix_conc.iloc[i, j]:.2f}',
                       ha="center", va="center", color="white" if abs(correlation_matrix_conc.iloc[i, j]) > 0.5 else "black",
                       fontweight='bold')

ax.set_xticks(range(len(correlation_matrix_conc.columns)))
ax.set_yticks(range(len(correlation_matrix_conc.columns)))
ax.set_xticklabels(correlation_matrix_conc.columns, rotation=45)
ax.set_yticklabels(correlation_matrix_conc.columns)
ax.set_title('Matriz de Correlação - Servidor Concorrente', fontsize=14, fontweight='bold')

# Barra de cores
cbar = plt.colorbar(im)
cbar.set_label('Correlação', rotation=270, labelpad=15)

plt.tight_layout()
plt.savefig('graficos/heatmap_correlacao_concorrente.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Gráfico 24 salvo: graficos/heatmap_correlacao_concorrente.png")

print("\n TODOS OS 24 GRÁFICOS FORAM GERADOS COM SUCESSO!")
print(" Pasta: graficos/")
print(" Gráficos gerados:")
print("   1-6.  Gráficos originais")
print("   7.    comparacao_throughput_get.png")
print("   8.    comparacao_throughput_post.png")
print("   9.    evolucao_throughput_get_sequencial.png")
print("   10.   evolucao_throughput_post_sequencial.png")
print("   11.   evolucao_throughput_get_concorrente.png")
print("   12.   evolucao_throughput_post_concorrente.png")
print("   13.   distribuicao_latencia_get_sequencial.png")
print("   14.   distribuicao_latencia_post_sequencial.png")
print("   15.   distribuicao_latencia_get_concorrente.png")
print("   16.   distribuicao_latencia_post_concorrente.png")
print("   17.   analise_falhas_get_concorrente.png")
print("   18.   analise_falhas_post_concorrente.png")
print("   19.   razao_get_post_sequencial.png")
print("   20.   razao_get_post_concorrente.png")
print("   21.   consistencia_sequencial.png")
print("   22.   consistencia_concorrente.png")
print("   23.   heatmap_correlacao_sequencial.png")
print("   24.   heatmap_correlacao_concorrente.png")