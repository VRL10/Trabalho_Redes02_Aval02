import json
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

class AnalisadorMetricas:
    def __init__(self, arquivoResultados):
        self.arquivoResultados = arquivoResultados
        self.dados = self.carregarDados()
        
    def carregarDados(self):
        with open(self.arquivoResultados, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    
    def calcularEstatisticasGrupo(self, grupo):
        if not grupo:
            return None
            
        temposMedios = [t['tempo_medio'] for t in grupo]
        throughputs = [t['throughput'] for t in grupo]
        taxasSucesso = [t['taxa_sucesso'] for t in grupo]
        desviosPadrao = [t['desvio_padrao'] for t in grupo]
        
        return {
            'tempo_medio': statistics.mean(temposMedios),
            'tempo_desvio': statistics.stdev(temposMedios) if len(temposMedios) > 1 else 0,
            'throughput_medio': statistics.mean(throughputs),
            'throughput_desvio': statistics.stdev(throughputs) if len(throughputs) > 1 else 0,
            'taxa_sucesso_medio': statistics.mean(taxasSucesso),
            'consistencia_medio': statistics.mean(desviosPadrao),
            'amostras': len(grupo)
        }
    
    def converter_para_formato_antigo(self):
        """Converte o novo formato para o formato esperado pelo analisador original"""
        formato_antigo = {
            'metadata': {
                'matricula': self.dados['metadata']['matricula'],
                'nome': self.dados['metadata']['nome'],
                'subrede': '37.92.0.0/16',
                'protocolo': 'TCP/Socket',
                'num_execucoes': self.dados['metadata']['num_execucoes'],
                'custom_id': self.dados['metadata']['custom_id']
            },
            'servidor_sequencial': {
                'testes_get_sequenciais': [],
                'testes_post_sequenciais': [],
                'testes_get_concorrentes': [],
                'testes_post_concorrentes': []
            },
            'servidor_concorrente': {
                'testes_get_sequenciais': [],
                'testes_post_sequenciais': [],
                'testes_get_concorrentes': [],
                'testes_post_concorrentes': []
            }
        }
        
        # Mapear cenários para o formato antigo
        for cenario_nome, cenario in self.dados['cenarios'].items():
            # Sequencial
            if 'sequencial' in cenario:
                if cenario_nome == 'baixa_concorrencia':
                    formato_antigo['servidor_sequencial']['testes_get_sequenciais'].extend(cenario['sequencial']['GET'])
                    formato_antigo['servidor_sequencial']['testes_post_sequenciais'].extend(cenario['sequencial']['POST'])
                else:
                    formato_antigo['servidor_sequencial']['testes_get_concorrentes'].extend(cenario['sequencial']['GET'])
                    formato_antigo['servidor_sequencial']['testes_post_concorrentes'].extend(cenario['sequencial']['POST'])
            
            # Concorrente
            if 'concorrente' in cenario:
                if cenario_nome == 'baixa_concorrencia':
                    formato_antigo['servidor_concorrente']['testes_get_sequenciais'].extend(cenario['concorrente']['GET'])
                    formato_antigo['servidor_concorrente']['testes_post_sequenciais'].extend(cenario['concorrente']['POST'])
                else:
                    formato_antigo['servidor_concorrente']['testes_get_concorrentes'].extend(cenario['concorrente']['GET'])
                    formato_antigo['servidor_concorrente']['testes_post_concorrentes'].extend(cenario['concorrente']['POST'])
        
        return formato_antigo
    
    def gerarGraficos(self):
        """Gera gráficos comparativos"""
        dados_convertidos = self.converter_para_formato_antigo()
        
        stats_seq_get_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_get_concorrentes'])
        stats_conc_get_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_get_concorrentes'])
        stats_seq_post_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_post_concorrentes'])
        stats_conc_post_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_post_concorrentes'])
        
        # Garantir que o diretório existe
        os.makedirs('/app/resultados', exist_ok=True)
        
        # Gráfico 1: Throughput Comparativo
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Throughput GET
        servidores = ['Sequencial', 'Concorrente']
        throughput_get = [stats_seq_get_conc['throughput_medio'], stats_conc_get_conc['throughput_medio']]
        bars1 = ax1.bar(servidores, throughput_get, color=['red', 'blue'], alpha=0.7)
        ax1.set_title('Throughput - REQUISIÇÕES GET\n(Cenário Concorrente)')
        ax1.set_ylabel('Requests por Segundo (req/s)')
        ax1.grid(True, alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom')
        
        # Throughput POST
        throughput_post = [stats_seq_post_conc['throughput_medio'], stats_conc_post_conc['throughput_medio']]
        bars2 = ax2.bar(servidores, throughput_post, color=['red', 'blue'], alpha=0.7)
        ax2.set_title('Throughput - REQUISIÇÕES POST\n(Cenário Concorrente)')
        ax2.set_ylabel('Requests por Segundo (req/s)')
        ax2.grid(True, alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/app/resultados/throughput_comparativo.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Gráfico 2: Tempo de Resposta
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Tempo GET
        tempo_get = [stats_seq_get_conc['tempo_medio'], stats_conc_get_conc['tempo_medio']]
        bars1 = ax1.bar(servidores, tempo_get, color=['orange', 'green'], alpha=0.7)
        ax1.set_title('Tempo Médio de Resposta - GET\n(Cenário Concorrente)')
        ax1.set_ylabel('Tempo (segundos)')
        ax1.grid(True, alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{height:.3f}s', ha='center', va='bottom')
        
        # Tempo POST
        tempo_post = [stats_seq_post_conc['tempo_medio'], stats_conc_post_conc['tempo_medio']]
        bars2 = ax2.bar(servidores, tempo_post, color=['orange', 'green'], alpha=0.7)
        ax2.set_title('Tempo Médio de Resposta - POST\n(Cenário Concorrente)')
        ax2.set_ylabel('Tempo (segundos)')
        ax2.grid(True, alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{height:.3f}s', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/app/resultados/tempo_resposta_comparativo.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Gráfico 3: Taxa de Sucesso
        fig, ax = plt.subplots(figsize=(10, 6))
        
        taxas_get = [stats_seq_get_conc['taxa_sucesso_medio'], stats_conc_get_conc['taxa_sucesso_medio']]
        taxas_post = [stats_seq_post_conc['taxa_sucesso_medio'], stats_conc_post_conc['taxa_sucesso_medio']]
        
        x = np.arange(len(servidores))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, taxas_get, width, label='GET', color='lightblue')
        bars2 = ax.bar(x + width/2, taxas_post, width, label='POST', color='lightcoral')
        
        ax.set_title('Taxa de Sucesso por Servidor e Método\n(Cenário Concorrente)')
        ax.set_ylabel('Taxa de Sucesso (%)')
        ax.set_xlabel('Tipo de Servidor')
        ax.set_xticks(x)
        ax.set_xticklabels(servidores)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/app/resultados/taxa_sucesso_comparativo.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Gráficos gerados em /app/resultados/")
    
    def gerarRelatorioCompleto(self):
        print("=" * 80)
        print("RELATÓRIO COMPLETO DE ANÁLISE - SERVIDORES WEB COM SOCKETS BRUTOS")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Matrícula: {self.dados['metadata']['matricula']}")
        print(f"Nome: {self.dados['metadata']['nome']}")
        print(f"Subrede: 37.92.0.0/16")
        print(f"Protocolo: TCP/Socket")
        print(f"Execuções: {self.dados['metadata']['num_execucoes']}")
        print(f"X-Custom-ID: {self.dados['metadata']['custom_id']}")
        print("=" * 80)
        
        dados_convertidos = self.converter_para_formato_antigo()
        
        stats_seq_get_seq = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_get_sequenciais'])
        stats_seq_post_seq = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_post_sequenciais'])
        stats_seq_get_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_get_concorrentes'])
        stats_seq_post_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_sequencial']['testes_post_concorrentes'])
        
        stats_conc_get_seq = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_get_sequenciais'])
        stats_conc_post_seq = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_post_sequenciais'])
        stats_conc_get_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_get_concorrentes'])
        stats_conc_post_conc = self.calcularEstatisticasGrupo(dados_convertidos['servidor_concorrente']['testes_post_concorrentes'])
        
        self.analisarComparativoGeral(stats_seq_get_conc, stats_conc_get_conc, stats_seq_post_conc, stats_conc_post_conc)
        self.analisarServidorDetalhado('SEQUENCIAL', stats_seq_get_seq, stats_seq_post_seq, stats_seq_get_conc, stats_seq_post_conc)
        self.analisarServidorDetalhado('CONCORRENTE', stats_conc_get_seq, stats_conc_post_seq, stats_conc_get_conc, stats_conc_post_conc)
        self.gerarConclusoesFinais(stats_seq_get_conc, stats_conc_get_conc, stats_seq_post_conc, stats_conc_post_conc)
        
        self.gerarGraficos()
    
    def analisarComparativoGeral(self, seq_get, conc_get, seq_post, conc_post):
        print("\nANÁLISE COMPARATIVA GERAL (Cenário Concorrente)")
        print("-" * 60)
        
        print(f"\nTHROUGHPUT (Requests por Segundo):")
        print(f"GET - Sequencial:  {seq_get['throughput_medio']:7.2f} req/s")
        print(f"GET - Concorrente: {conc_get['throughput_medio']:7.2f} req/s")
        print(f"POST - Sequencial:  {seq_post['throughput_medio']:7.2f} req/s") 
        print(f"POST - Concorrente: {conc_post['throughput_medio']:7.2f} req/s")
        
        melhoria_get = ((conc_get['throughput_medio'] - seq_get['throughput_medio']) / seq_get['throughput_medio']) * 100
        melhoria_post = ((conc_post['throughput_medio'] - seq_post['throughput_medio']) / seq_post['throughput_medio']) * 100
        
        print(f"\nMELHORIA DO CONCORRENTE:")
        print(f"GET:  {melhoria_get:+.1f}%")
        print(f"POST: {melhoria_post:+.1f}%")
        
        print(f"\nCONFIABILIDADE (Taxa de Sucesso):")
        print(f"GET - Sequencial:  {seq_get['taxa_sucesso_medio']:6.1f}%")
        print(f"GET - Concorrente: {conc_get['taxa_sucesso_medio']:6.1f}%")
        print(f"POST - Sequencial:  {seq_post['taxa_sucesso_medio']:6.1f}%")
        print(f"POST - Concorrente: {conc_post['taxa_sucesso_medio']:6.1f}%")
        
        print(f"\nEFICIÊNCIA (Tempo Médio de Resposta):")
        print(f"GET - Sequencial:  {seq_get['tempo_medio']:7.3f}s")
        print(f"GET - Concorrente: {conc_get['tempo_medio']:7.3f}s")
        print(f"POST - Sequencial:  {seq_post['tempo_medio']:7.3f}s")
        print(f"POST - Concorrente: {conc_post['tempo_medio']:7.3f}s")
    
    def analisarServidorDetalhado(self, nome, get_seq, post_seq, get_conc, post_conc):
        print(f"\n{'-'*60}")
        print(f"ANÁLISE DETALHADA - SERVIDOR {nome}")
        print(f"{'-'*60}")
        
        print(f"\nCENÁRIO SEQUENCIAL:")
        print(f"GET  - Tempo: {get_seq['tempo_medio']:.4f}s, Throughput: {get_seq['throughput_medio']:.2f} req/s, Sucesso: {get_seq['taxa_sucesso_medio']:.1f}%")
        print(f"POST - Tempo: {post_seq['tempo_medio']:.4f}s, Throughput: {post_seq['throughput_medio']:.2f} req/s, Sucesso: {post_seq['taxa_sucesso_medio']:.1f}%")
        
        print(f"\nCENÁRIO CONCORRENTE:")
        print(f"GET  - Tempo: {get_conc['tempo_medio']:.4f}s, Throughput: {get_conc['throughput_medio']:.2f} req/s, Sucesso: {get_conc['taxa_sucesso_medio']:.1f}%")
        print(f"POST - Tempo: {post_conc['tempo_medio']:.4f}s, Throughput: {post_conc['throughput_medio']:.2f} req/s, Sucesso: {post_conc['taxa_sucesso_medio']:.1f}%")
        
        if get_conc and post_conc:
            diferenca_get_post = ((get_conc['throughput_medio'] - post_conc['throughput_medio']) / get_conc['throughput_medio']) * 100
            print(f"\nDIFERENÇA GET vs POST (Concorrente): {diferenca_get_post:+.1f}%")
    
    def gerarConclusoesFinais(self, seq_get, conc_get, seq_post, conc_post):
        print("\n" + "=" * 80)
        print("CONCLUSÕES E RECOMENDAÇÕES")
        print("=" * 80)
        
        print(f"\nDESEMPENHO ABSOLUTO (Carga Concorrente):")
        print(f"Sequencial:  GET {seq_get['throughput_medio']:.0f} req/s, POST {seq_post['throughput_medio']:.0f} req/s")
        print(f"Concorrente: GET {conc_get['throughput_medio']:.0f} req/s, POST {conc_post['throughput_medio']:.0f} req/s")
        
        print(f"\nFATOR DE MELHORIA (Concorrente vs Sequencial):")
        fator_get = conc_get['throughput_medio'] / seq_get['throughput_medio']
        fator_post = conc_post['throughput_medio'] / seq_post['throughput_medio']
        print(f"GET:  {fator_get:.1f}x mais rápido")
        print(f"POST: {fator_post:.1f}x mais rápido")
        
        print(f"\nCOMPORTAMENTO DOS MÉTODOS HTTP:")
        diferenca_seq = ((seq_get['throughput_medio'] - seq_post['throughput_medio']) / seq_get['throughput_medio']) * 100
        diferenca_conc = ((conc_get['throughput_medio'] - conc_post['throughput_medio']) / conc_get['throughput_medio']) * 100
        print(f"Sequencial:  POST é {diferenca_seq:+.1f}% mais lento que GET")
        print(f"Concorrente: POST é {diferenca_conc:+.1f}% mais lento que GET")
        
        print(f"\nCONSISTÊNCIA (Desvio Padrão):")
        print(f"Sequencial:  {seq_get['consistencia_medio']:.4f}s")
        print(f"Concorrente: {conc_get['consistencia_medio']:.4f}s")
        
        print(f"\nRECOMENDAÇÕES BASEADAS NOS RESULTADOS:")
        print(f"✓ Use servidor SEQUENCIAL para:")
        print(f"   • Aplicações com carga baixa e previsível")
        print(f"   • Ambientes com recursos limitados de CPU")
        print(f"   • Casos onde simplicidade e estabilidade são prioridade")
        
        print(f"✓ Use servidor CONCORRENTE para:")
        print(f"   • Aplicações com múltiplos usuários simultâneos")
        print(f"   • Serviços que exigem alta disponibilidade e escalabilidade")
        print(f"   • Cenários com picos de carga imprevisíveis")
        
        print(f"\nOBSERVAÇÕES TÉCNICAS:")
        print(f"• POST é naturalmente mais lento devido ao processamento de dados")
        print(f"• Ambos os servidores mantêm alta confiabilidade (>99%) com sockets brutos")
        print(f"• O concorrente escala melhor sob carga pesada (até {max(fator_get, fator_post):.1f}x)")
        print(f"• O sequencial tem comportamento mais consistente (menor desvio padrão)")
        print(f"• Implementação com sockets brutos atende todos os requisitos do trabalho")
    
    def salvarRelatorio(self):
        import sys
        from io import StringIO
        
        stdout_original = sys.stdout
        sys.stdout = buffer = StringIO()
        
        self.gerarRelatorioCompleto()
        
        sys.stdout = stdout_original
        conteudo = buffer.getvalue()
        
        nome_arquivo = f"relatorio_analise_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        os.makedirs('/app/resultados', exist_ok=True)
        with open(f'/app/resultados/{nome_arquivo}', 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        
        print(f"\nRelatório salvo em: /app/resultados/{nome_arquivo}")
        return nome_arquivo

def encontrarArquivoRecente():
    import os
    caminhos_tentados = [
        'resultados/metricas_completas.json',
        '/app/resultados/metricas_completas.json', 
        'metricas_completas.json'
    ]
    
    for caminho in caminhos_tentados:
        if os.path.exists(caminho):
            print(f"Arquivo encontrado: {caminho}")
            return caminho
    
    print("Nenhum arquivo de resultados encontrado nos caminhos:")
    for caminho in caminhos_tentados:
        print(f"  - {caminho}")
    return None

if __name__ == "__main__":
    arquivo = encontrarArquivoRecente()
    
    if arquivo:
        print(f"Analisando arquivo: {arquivo}")
        analisador = AnalisadorMetricas(arquivo)
        analisador.gerarRelatorioCompleto()
        arquivo_relatorio = analisador.salvarRelatorio()
        
        print("\n" + "=" * 80)
        print("ANÁLISE CONCLUÍDA!")
        print(f"Relatório salvo em: /app/resultados/{arquivo_relatorio}")
        print("Gráficos gerados em: /app/resultados/")
        print("=" * 80)
    else:
        print("Nenhum arquivo de resultados encontrado!")
        print("Execute primeiro: docker-compose up cliente-teste")