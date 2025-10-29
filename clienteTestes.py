import socket
import time
import statistics
import threading
import hashlib
import json
from datetime import datetime
import os

class ClienteTestesServidores:
    def __init__(self):
        self.id_personalizado = hashlib.md5("20229043792 Victor Rodrigues Luz".encode()).hexdigest()
    
    def criar_requisicao_http(self, caminho="/", ip_alvo="37.92.0.10"):
        requisicao = f"""GET {caminho} HTTP/1.1\r
Host: {ip_alvo}\r
X-Custom-ID: {self.id_personalizado}\r
User-Agent: Cliente-Teste-Sockets/Redes-II\r
Connection: close\r
\r
"""
        return requisicao
    
    def medir_requisicao(self, ip, porta, caminho="/"):
        inicio = time.time()
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((ip, porta))
            
            requisicao = self.criar_requisicao_http(caminho, ip)
            s.send(requisicao.encode())
            
            resposta = b""
            while True:
                dados = s.recv(4096)
                if not dados:
                    break
                resposta += dados
            
            tempo = time.time() - inicio
            s.close()
            
            resposta_str = resposta.decode('utf-8', errors='ignore')
            if '200 OK' in resposta_str:
                return tempo, 200, True
            else:
                return tempo, 400, False
                
        except Exception as e:
            print(f"Erro na requisição para {ip}:{porta}: {e}")
            return time.time() - inicio, 0, False
    
    def executar_teste_servidor(self, ip, porta, num_threads, requisicoes_por_thread):
        total_requisicoes = num_threads * requisicoes_por_thread
        
        print(f"Teste Servidor {ip}:{porta} - {num_threads} threads × {requisicoes_por_thread} reqs = {total_requisicoes} total")
        
        resultados = {
            'tempos': [],
            'sucessos': 0,
            'lock': threading.Lock()
        }
        
        def thread_trabalhadora(id_thread):
            for i in range(requisicoes_por_thread):
                caminho = "/" if i % 2 == 0 else "/info"
                
                tempo, status, sucesso = self.medir_requisicao(ip, porta, caminho)
                
                with resultados['lock']:
                    resultados['tempos'].append(tempo)
                    if sucesso:
                        resultados['sucessos'] += 1
        
        threads = []
        inicio_teste = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=thread_trabalhadora, args=(i + 1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tempo_total = time.time() - inicio_teste
        
        return {
            'ip': ip,
            'porta': porta,
            'total_requisicoes': total_requisicoes,
            'threads': num_threads,
            'requisicoes_por_thread': requisicoes_por_thread,
            'sucessos': resultados['sucessos'],
            'falhas': total_requisicoes - resultados['sucessos'],
            'taxa_sucesso': (resultados['sucessos'] / total_requisicoes) * 100,
            'tempo_total': tempo_total,
            'tempo_medio': statistics.mean(resultados['tempos']) if resultados['tempos'] else 0,
            'tempo_minimo': min(resultados['tempos']) if resultados['tempos'] else 0,
            'tempo_maximo': max(resultados['tempos']) if resultados['tempos'] else 0,
            'desvio_padrao': statistics.stdev(resultados['tempos']) if len(resultados['tempos']) > 1 else 0,
            'throughput': total_requisicoes / tempo_total if tempo_total > 0 else 0
        }
    
    def executar_suite_comparativa_servidores(self, num_execucoes=10):
        print("=" * 70)
        print("SUITE DE TESTES - COMPARAÇÃO SERVIDORES SEQUENCIAL vs CONCORRENTE")
        print("=" * 70)
        print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Execuções por cenário: {num_execucoes}")
        print(f"X-Custom-ID: {self.id_personalizado}")
        print("IPs baseados na matrícula 20229043792 → 3792")
        print("Servidor Sequencial: 37.92.0.10:80")
        print("Servidor Concorrente: 37.92.0.11:80")
        print("=" * 70)
        
        resultados = {
            'metadata': {
                'matricula': '20229043792',
                'nome': 'Victor Rodrigues Luz',
                'data_testes': datetime.now().isoformat(),
                'num_execucoes': num_execucoes,
                'custom_id': self.id_personalizado,
                'configuracao': 'comparacao_servidores_sequencial_vs_concorrente',
                'metricas': ['throughput', 'tempo_medio', 'taxa_sucesso', 'desvio_padrao']
            },
            'cenarios': {}
        }
        
        cenarios = [
            {'nome': 'carga_baixa', 'threads': 1, 'reqs_por_thread': 10},
            {'nome': 'carga_media', 'threads': 5, 'reqs_por_thread': 4},
            {'nome': 'carga_alta', 'threads': 10, 'reqs_por_thread': 3}
        ]
        
        servidores = [
            {'nome': 'sequencial', 'ip': '37.92.0.10', 'porta': 80},
            {'nome': 'concorrente', 'ip': '37.92.0.11', 'porta': 80}
        ]
        
        for cenario in cenarios:
            nome_cenario = cenario['nome']
            resultados['cenarios'][nome_cenario] = {}
            
            print(f"\n{'='*50}")
            print(f"CENÁRIO: {nome_cenario.upper().replace('_', ' ')}")
            print(f"Threads: {cenario['threads']}, Reqs/thread: {cenario['reqs_por_thread']}")
            print(f"Total: {cenario['threads'] * cenario['reqs_por_thread']} requisições")
            print(f"{'='*50}")
            
            for servidor in servidores:
                print(f"\n--- SERVIDOR {servidor['nome'].upper()} ---")
                
                resultados_servidor = []
                
                for execucao in range(num_execucoes):
                    print(f"Execução {execucao + 1}/{num_execucoes}")
                    
                    resultado = self.executar_teste_servidor(
                        servidor['ip'], servidor['porta'],
                        cenario['threads'], cenario['reqs_por_thread']
                    )
                    resultados_servidor.append(resultado)
                    time.sleep(0.5)
                
                resultados['cenarios'][nome_cenario][servidor['nome']] = resultados_servidor
        
        os.makedirs('resultados', exist_ok=True)
        with open('resultados/metricas_completas.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        self.gerar_relatorio_comparativo_servidores(resultados)
        
        return resultados
    
    def gerar_relatorio_comparativo_servidores(self, resultados):
        print("\n" + "=" * 70)
        print("RELAToRIO COMPARATIVO - SERVIDORES SEQUENCIAL vs CONCORRENTE")
        print("=" * 70)
        
        for cenario_nome, cenario in resultados['cenarios'].items():
            print(f"\n{cenario_nome.upper().replace('_', ' ')}:")
            
            for servidor_nome, servidor in cenario.items():
                tempos_medio = statistics.mean([r['tempo_medio'] for r in servidor])
                throughput_medio = statistics.mean([r['throughput'] for r in servidor])
                sucesso_medio = statistics.mean([r['taxa_sucesso'] for r in servidor])
                consistencia = statistics.mean([r['desvio_padrao'] for r in servidor])
                
                print(f"  {servidor_nome.upper()} | Throughput: {throughput_medio:6.1f} req/s")
                print(f"  | Tempo medio: {tempos_medio:6.3f}s")
                print(f"  | Sucesso: {sucesso_medio:6.1f}%")
                print(f"  | Consistencia: {consistencia:6.4f}s")

if __name__ == "__main__":
    cliente = ClienteTestesServidores()
    resultados = cliente.executar_suite_comparativa_servidores(num_execucoes=10)
    
    print("\n" + "=" * 70)
    print(" SUITE DE TESTES concluida!")
    print("=" * 70)
    print("Resultados salvs em: resultados/metricas_completas.json")
    print("Analise focada na comparacao: Servidor Sequencial vs Concorrente")
    print("=" * 70)