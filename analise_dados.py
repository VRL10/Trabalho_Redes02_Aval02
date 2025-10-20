"""
Analisador de Dados - Redes de Computadores II
Analisa resultados de testes GET e POST separadamente
Autor: Victor Rodrigues Luz - Matricula: 20229043792
"""

import json
import statistics
from datetime import datetime

class AnalisadorDados:
    def __init__(self, arquivo_resultados):
        self.arquivo_resultados = arquivo_resultados
        self.dados = self.carregarDados()
        
    def carregarDados(self):
        with open(self.arquivo_resultados, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def gerarRelatorioCompleto(self):
        print("=" * 80)
        print("RELATORIO DE ANALISE DE DESEMPENHO - GET E POST")
        print("=" * 80)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Matricula: {self.dados['metadata']['matricula']}")
        print(f"Nome: {self.dados['metadata']['nome']}")
        print(f"Execucoes: {self.dados['metadata']['num_execucoes']}")
        print("=" * 80)
        
        # Analise comparativa geral
        self.analisarComparativoGeral()
        
        # Analise detalhada por servidor e metodo
        print("\n" + "=" * 80)
        print("ANALISE DETALHADA POR SERVIDOR E METODO")
        print("=" * 80)
        
        self.analisarServidor('servidor_sequencial', 'SEQUENCIAL')
        self.analisarServidor('servidor_concorrente', 'CONCORRENTE')
        
        # Conclusoes
        self.gerarConclusoes()
    
    def analisarComparativoGeral(self):
        print("\nCOMPARACAO GERAL ENTRE SERVIDORES")
        print("-" * 50)
        
        # Dados para comparacao - usando cenario concorrente (mais relevante)
        seq_get_conc = self.dados['servidor_sequencial']['testes_get_concorrentes']
        seq_post_conc = self.dados['servidor_sequencial']['testes_post_concorrentes']
        conc_get_conc = self.dados['servidor_concorrente']['testes_get_concorrentes']
        conc_post_conc = self.dados['servidor_concorrente']['testes_post_concorrentes']
        
        # Calcula metricas medias
        thr_seq_get = statistics.mean([d['requisicoes_segundo'] for d in seq_get_conc])
        thr_seq_post = statistics.mean([d['requisicoes_segundo'] for d in seq_post_conc])
        thr_conc_get = statistics.mean([d['requisicoes_segundo'] for d in conc_get_conc])
        thr_conc_post = statistics.mean([d['requisicoes_segundo'] for d in conc_post_conc])
        
        print(f"\nTHROUGHPUT EM CARGA CONCORRENTE:")
        print(f"Sequencial - GET:  {thr_seq_get:.2f} req/s")
        print(f"Sequencial - POST: {thr_seq_post:.2f} req/s")
        print(f"Concorrente - GET:  {thr_conc_get:.2f} req/s")
        print(f"Concorrente - POST: {thr_conc_post:.2f} req/s")
        
        # Melhorias
        melhoria_get = ((thr_conc_get - thr_seq_get) / thr_seq_get) * 100
        melhoria_post = ((thr_conc_post - thr_seq_post) / thr_seq_post) * 100
        
        print(f"\nMELHORIA DO CONCORRENTE:")
        print(f"GET:  +{melhoria_get:.1f}%")
        print(f"POST: +{melhoria_post:.1f}%")
    
    def analisarServidor(self, servidor, nome):
        print(f"\n--- SERVIDOR {nome} ---")
        
        dados_get_seq = self.dados[servidor]['testes_get_sequenciais']
        dados_post_seq = self.dados[servidor]['testes_post_sequenciais']
        dados_get_conc = self.dados[servidor]['testes_get_concorrentes']
        dados_post_conc = self.dados[servidor]['testes_post_concorrentes']
        
        print(f"\nCENARIO SEQUENCIAL:")
        self.imprimirMetricasMetodo(dados_get_seq, "GET")
        self.imprimirMetricasMetodo(dados_post_seq, "POST")
        
        print(f"\nCENARIO CONCORRENTE:")
        self.imprimirMetricasMetodo(dados_get_conc, "GET")
        self.imprimirMetricasMetodo(dados_post_conc, "POST")
        
        # Analise de diferenca entre GET e POST
        if dados_get_conc and dados_post_conc:
            thr_get = statistics.mean([d['requisicoes_segundo'] for d in dados_get_conc])
            thr_post = statistics.mean([d['requisicoes_segundo'] for d in dados_post_conc])
            
            diferenca = ((thr_get - thr_post) / thr_get) * 100
            print(f"\nDIFERENCA GET vs POST (concorrente): {diferenca:+.1f}%")
    
    def imprimirMetricasMetodo(self, dados_grupo, metodo):
        if not dados_grupo:
            print(f"  {metodo}: Sem dados disponiveis")
            return
        
        tempos_medios = [d['tempo_medio'] for d in dados_grupo]
        throughputs = [d['requisicoes_segundo'] for d in dados_grupo]
        taxas_sucesso = [d['taxa_sucesso'] for d in dados_grupo]
        
        print(f"  {metodo}:")
        print(f"    Throughput: {statistics.mean(throughputs):.2f} req/s")
        print(f"    Tempo Medio: {statistics.mean(tempos_medios):.4f}s")
        print(f"    Sucesso: {statistics.mean(taxas_sucesso):.1f}%")
    
    def gerarConclusoes(self):
        print("\n" + "=" * 80)
        print("CONCLUSOES E RECOMENDACOES")
        print("=" * 80)
        
        # Dados para conclusoes
        seq_get_conc = self.dados['servidor_sequencial']['testes_get_concorrentes']
        seq_post_conc = self.dados['servidor_sequencial']['testes_post_concorrentes']
        conc_get_conc = self.dados['servidor_concorrente']['testes_get_concorrentes']
        conc_post_conc = self.dados['servidor_concorrente']['testes_post_concorrentes']
        
        # Calculos finais
        thr_seq_get = statistics.mean([d['requisicoes_segundo'] for d in seq_get_conc])
        thr_seq_post = statistics.mean([d['requisicoes_segundo'] for d in seq_post_conc])
        thr_conc_get = statistics.mean([d['requisicoes_segundo'] for d in conc_get_conc])
        thr_conc_post = statistics.mean([d['requisicoes_segundo'] for d in conc_post_conc])
        
        print(f"\nDESEMPENHO ABSOLUTO (carga concorrente):")
        print(f"- Sequencial: GET {thr_seq_get:.0f} req/s, POST {thr_seq_post:.0f} req/s")
        print(f"- Concorrente: GET {thr_conc_get:.0f} req/s, POST {thr_conc_post:.0f} req/s")
        
        print(f"\nFATOR DE MELHORIA DO CONCORRENTE:")
        fator_get = thr_conc_get / thr_seq_get
        fator_post = thr_conc_post / thr_seq_post
        print(f"- GET: {fator_get:.1f}x mais rapido")
        print(f"- POST: {fator_post:.1f}x mais rapido")
        
        print(f"\nCOMPORTAMENTO DOS METODOS HTTP:")
        diferenca_seq = ((thr_seq_get - thr_seq_post) / thr_seq_get) * 100
        diferenca_conc = ((thr_conc_get - thr_conc_post) / thr_conc_get) * 100
        print(f"- Sequencial: POST e {diferenca_seq:+.1f}% mais lento que GET")
        print(f"- Concorrente: POST e {diferenca_conc:+.1f}% mais lento que GET")
        
        print(f"\nRECOMENDACOES:")
        print(f"- Use servidor SEQUENCIAL para aplicacoes com carga baixa e previsivel")
        print(f"- Use servidor CONCORRENTE para aplicacoes com multiplos usuarios simultaneos")
        print(f"- POST e naturalmente mais lento devido ao processamento de dados")
        print(f"- Ambos os servidores mantem 100% de confiabilidade")
    
    def salvarRelatorioTexto(self):
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        self.gerarRelatorioCompleto()
        
        sys.stdout = old_stdout
        conteudo = buffer.getvalue()
        
        filename = f"relatorio_completo_get_post.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"\nRelatorio salvo em: {filename}")
        return filename

def encontrarArquivoRecente():
    import glob
    import os
    
    locais = [
        'resultados/metricas_completas_get_post.json',
        'metricas_completas_get_post.json',
        'resultados/metricas_resultados.json',
        'metricas_resultados.json'
    ]
    
    for arquivo in locais:
        if os.path.exists(arquivo):
            return arquivo
    
    return None

if __name__ == "__main__":
    arquivo = encontrarArquivoRecente()
    
    if arquivo:
        print(f"Analisando arquivo: {arquivo}")
        analisador = AnalisadorDados(arquivo)
        analisador.gerarRelatorioCompleto()
        arquivo_relatorio = analisador.salvarRelatorioTexto()
        
        print("\n" + "=" * 80)
        print("ANALISE CONCLUIDA!")
        print(f"Relatorio salvo em: {arquivo_relatorio}")
        print("=" * 80)
    else:
        print("Nenhum arquivo de resultados encontrado!")
        print("Execute primeiro: python test_metricas.py")