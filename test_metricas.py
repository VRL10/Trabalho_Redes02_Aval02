"""
Script de Testes de Métricas - Redes de Computadores II
Executa testes automatizados para comparar desempenho dos servidores
Testa métodos GET e POST separadamente
Autor: Victor Rodrigues Luz - Matrícula: 20229043792
"""

import socket
import hashlib
import time
import statistics
import threading
import json
from datetime import datetime

class TesteMetricas:
    def __init__(self):
        self.customID = self.calcularCustomID()
        # IPs DOS CONTAINERS DOCKER
        self.servidor_sequencial_ip = "43.79.0.10"
        self.servidor_concorrente_ip = "43.79.0.11"
        self.porta = 80  # PORTA INTERNA DOS CONTAINERS
        
    def calcularCustomID(self):
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def criarRequisicaoGET(self, host, path="/"):
        requisicao = f"""GET {path} HTTP/1.1
Host: {host}
X-Custom-ID: {self.customID}
User-Agent: Teste-Metricas-Redes-II
Connection: close

"""
        return requisicao.replace('\n', '\r\n')
    
    def criarRequisicaoPOST(self, host, path="/submit", dados="teste=metricas"):
        requisicao = f"""POST {path} HTTP/1.1
Host: {host}
X-Custom-ID: {self.customID}
User-Agent: Teste-Metricas-Redes-II
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(dados)}
Connection: close

{dados}"""
        return requisicao.replace('\n', '\r\n')
    
    def medirRequisicaoGET(self, host, porta, path="/"):
        start_time = time.time()
        sucesso = False
        status_code = 0
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, porta))
            
            requisicao = self.criarRequisicaoGET(host, path)
            sock.sendall(requisicao.encode())
            
            resposta = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                resposta += data
            
            tempo_resposta = time.time() - start_time
            
            resposta_str = resposta.decode('utf-8')
            if '200 OK' in resposta_str:
                sucesso = True
                status_code = 200
            elif '400' in resposta_str:
                status_code = 400
            elif '404' in resposta_str:
                status_code = 404
            elif '500' in resposta_str:
                status_code = 500
                
            sock.close()
            return tempo_resposta, status_code, sucesso
            
        except Exception as e:
            print(f"Erro na requisição GET para {host}:{porta}: {e}")
            tempo_resposta = time.time() - start_time
            return tempo_resposta, 0, False
    
    def medirRequisicaoPOST(self, host, porta, path="/submit", dados="teste=metricas"):
        start_time = time.time()
        sucesso = False
        status_code = 0
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, porta))
            
            requisicao = self.criarRequisicaoPOST(host, path, dados)
            sock.sendall(requisicao.encode())
            
            resposta = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                resposta += data
            
            tempo_resposta = time.time() - start_time
            
            resposta_str = resposta.decode('utf-8')
            if '200 OK' in resposta_str:
                sucesso = True
                status_code = 200
            elif '400' in resposta_str:
                status_code = 400
            elif '404' in resposta_str:
                status_code = 404
            elif '500' in resposta_str:
                status_code = 500
                
            sock.close()
            return tempo_resposta, status_code, sucesso
            
        except Exception as e:
            print(f"Erro na requisição POST para {host}:{porta}: {e}")
            tempo_resposta = time.time() - start_time
            return tempo_resposta, 0, False
    
    def executarTesteSequencialGET(self, host, porta, num_requisicoes=25):
        print(f"Executando teste sequencial GET: {host}:{porta} - {num_requisicoes} requisições")
        
        tempos = []
        sucessos = 0
        falhas = 0
        start_time = time.time()
        
        for i in range(num_requisicoes):
            tempo, status, sucesso = self.medirRequisicaoGET(host, porta, "/")
            tempos.append(tempo)
            
            if sucesso:
                sucessos += 1
            else:
                falhas += 1
            
            if (i + 1) % 10 == 0:
                print(f"  GET Concluídas: {i + 1}/{num_requisicoes}")
        
        tempo_total = time.time() - start_time
        
        if tempos:
            tempos_ordenados = sorted(tempos)
            n = len(tempos_ordenados)
            mediana = tempos_ordenados[n // 2] if n % 2 == 1 else (tempos_ordenados[n // 2 - 1] + tempos_ordenados[n // 2]) / 2
            percentil_95 = tempos_ordenados[int(0.95 * n)] if n > 0 else 0
            percentil_99 = tempos_ordenados[int(0.99 * n)] if n > 0 else 0
            
            metricas = {
                'metodo': 'GET',
                'host': host,
                'porta': porta,
                'total_requisicoes': num_requisicoes,
                'sucessos': sucessos,
                'falhas': falhas,
                'taxa_sucesso': (sucessos / num_requisicoes) * 100,
                'tempo_total': tempo_total,
                'tempo_medio': statistics.mean(tempos),
                'tempo_mediana': mediana,
                'desvio_padrao': statistics.stdev(tempos) if len(tempos) > 1 else 0,
                'tempo_minimo': min(tempos),
                'tempo_maximo': max(tempos),
                'percentil_95': percentil_95,
                'percentil_99': percentil_99,
                'requisicoes_segundo': num_requisicoes / tempo_total if tempo_total > 0 else 0
            }
        else:
            metricas = {}
        
        return metricas
    
    def executarTesteSequencialPOST(self, host, porta, num_requisicoes=25):
        print(f"Executando teste sequencial POST: {host}:{porta} - {num_requisicoes} requisições")
        
        tempos = []
        sucessos = 0
        falhas = 0
        start_time = time.time()
        
        for i in range(num_requisicoes):
            tempo, status, sucesso = self.medirRequisicaoPOST(host, porta, "/submit", f"dados=teste_{i}")
            tempos.append(tempo)
            
            if sucesso:
                sucessos += 1
            else:
                falhas += 1
            
            if (i + 1) % 10 == 0:
                print(f"  POST Concluídas: {i + 1}/{num_requisicoes}")
        
        tempo_total = time.time() - start_time
        
        if tempos:
            tempos_ordenados = sorted(tempos)
            n = len(tempos_ordenados)
            mediana = tempos_ordenados[n // 2] if n % 2 == 1 else (tempos_ordenados[n // 2 - 1] + tempos_ordenados[n // 2]) / 2
            percentil_95 = tempos_ordenados[int(0.95 * n)] if n > 0 else 0
            percentil_99 = tempos_ordenados[int(0.99 * n)] if n > 0 else 0
            
            metricas = {
                'metodo': 'POST',
                'host': host,
                'porta': porta,
                'total_requisicoes': num_requisicoes,
                'sucessos': sucessos,
                'falhas': falhas,
                'taxa_sucesso': (sucessos / num_requisicoes) * 100,
                'tempo_total': tempo_total,
                'tempo_medio': statistics.mean(tempos),
                'tempo_mediana': mediana,
                'desvio_padrao': statistics.stdev(tempos) if len(tempos) > 1 else 0,
                'tempo_minimo': min(tempos),
                'tempo_maximo': max(tempos),
                'percentil_95': percentil_95,
                'percentil_99': percentil_99,
                'requisicoes_segundo': num_requisicoes / tempo_total if tempo_total > 0 else 0
            }
        else:
            metricas = {}
        
        return metricas
    
    def executarTesteConcorrenteGET(self, host, porta, num_threads=5, requisicoes_por_thread=10):
        print(f"Executando teste concorrente GET: {host}:{porta} - {num_threads} threads, {requisicoes_por_thread} reqs/thread")
        
        resultados = {
            'tempos': [],
            'sucessos': 0,
            'falhas': 0,
            'lock': threading.Lock()
        }
        
        def worker_thread(thread_id):
            for i in range(requisicoes_por_thread):
                tempo, status, sucesso = self.medirRequisicaoGET(host, porta, "/")
                
                with resultados['lock']:
                    resultados['tempos'].append(tempo)
                    if sucesso:
                        resultados['sucessos'] += 1
                    else:
                        resultados['falhas'] += 1
        
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(i + 1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tempo_total = time.time() - start_time
        total_requisicoes = num_threads * requisicoes_por_thread
        
        if resultados['tempos']:
            tempos_ordenados = sorted(resultados['tempos'])
            n = len(tempos_ordenados)
            mediana = tempos_ordenados[n // 2] if n % 2 == 1 else (tempos_ordenados[n // 2 - 1] + tempos_ordenados[n // 2]) / 2
            percentil_95 = tempos_ordenados[int(0.95 * n)] if n > 0 else 0
            percentil_99 = tempos_ordenados[int(0.99 * n)] if n > 0 else 0
            
            metricas = {
                'metodo': 'GET',
                'host': host,
                'porta': porta,
                'total_requisicoes': total_requisicoes,
                'threads': num_threads,
                'requisicoes_por_thread': requisicoes_por_thread,
                'sucessos': resultados['sucessos'],
                'falhas': resultados['falhas'],
                'taxa_sucesso': (resultados['sucessos'] / total_requisicoes) * 100,
                'tempo_total': tempo_total,
                'tempo_medio': statistics.mean(resultados['tempos']),
                'tempo_mediana': mediana,
                'desvio_padrao': statistics.stdev(resultados['tempos']) if len(resultados['tempos']) > 1 else 0,
                'tempo_minimo': min(resultados['tempos']),
                'tempo_maximo': max(resultados['tempos']),
                'percentil_95': percentil_95,
                'percentil_99': percentil_99,
                'requisicoes_segundo': total_requisicoes / tempo_total if tempo_total > 0 else 0
            }
        else:
            metricas = {}
        
        return metricas
    
    def executarTesteConcorrentePOST(self, host, porta, num_threads=5, requisicoes_por_thread=10):
        print(f"Executando teste concorrente POST: {host}:{porta} - {num_threads} threads, {requisicoes_por_thread} reqs/thread")
        
        resultados = {
            'tempos': [],
            'sucessos': 0,
            'falhas': 0,
            'lock': threading.Lock()
        }
        
        def worker_thread(thread_id):
            for i in range(requisicoes_por_thread):
                tempo, status, sucesso = self.medirRequisicaoPOST(host, porta, "/submit", f"dados=thread_{thread_id}_req_{i}")
                
                with resultados['lock']:
                    resultados['tempos'].append(tempo)
                    if sucesso:
                        resultados['sucessos'] += 1
                    else:
                        resultados['falhas'] += 1
        
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(i + 1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tempo_total = time.time() - start_time
        total_requisicoes = num_threads * requisicoes_por_thread
        
        if resultados['tempos']:
            tempos_ordenados = sorted(resultados['tempos'])
            n = len(tempos_ordenados)
            mediana = tempos_ordenados[n // 2] if n % 2 == 1 else (tempos_ordenados[n // 2 - 1] + tempos_ordenados[n // 2]) / 2
            percentil_95 = tempos_ordenados[int(0.95 * n)] if n > 0 else 0
            percentil_99 = tempos_ordenados[int(0.99 * n)] if n > 0 else 0
            
            metricas = {
                'metodo': 'POST',
                'host': host,
                'porta': porta,
                'total_requisicoes': total_requisicoes,
                'threads': num_threads,
                'requisicoes_por_thread': requisicoes_por_thread,
                'sucessos': resultados['sucessos'],
                'falhas': resultados['falhas'],
                'taxa_sucesso': (resultados['sucessos'] / total_requisicoes) * 100,
                'tempo_total': tempo_total,
                'tempo_medio': statistics.mean(resultados['tempos']),
                'tempo_mediana': mediana,
                'desvio_padrao': statistics.stdev(resultados['tempos']) if len(resultados['tempos']) > 1 else 0,
                'tempo_minimo': min(resultados['tempos']),
                'tempo_maximo': max(resultados['tempos']),
                'percentil_95': percentil_95,
                'percentil_99': percentil_99,
                'requisicoes_segundo': total_requisicoes / tempo_total if tempo_total > 0 else 0
            }
        else:
            metricas = {}
        
        return metricas
    
    def executarSuiteCompleta(self, num_execucoes=10):  # MUDADO: 10 execuções conforme pedido
        print("=" * 70)
        print("SUITE COMPLETA DE TESTES - GET E POST (DOCKER)")
        print("=" * 70)
        print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Execuções por teste: {num_execucoes}")
        print(f"Servidor Sequencial: {self.servidor_sequencial_ip}:{self.porta}")
        print(f"Servidor Concorrente: {self.servidor_concorrente_ip}:{self.porta}")
        print("=" * 70)
        
        resultados = {
            'metadata': {
                'matricula': '20229043792',
                'nome': 'Victor Rodrigues Luz',
                'data_testes': datetime.now().isoformat(),
                'num_execucoes': num_execucoes,
                'custom_id': self.customID,
                'servidor_sequencial': f"{self.servidor_sequencial_ip}:{self.porta}",
                'servidor_concorrente': f"{self.servidor_concorrente_ip}:{self.porta}",
                'descricao_testes': 'Testes Docker - GET e POST em cenários sequenciais e concorrentes'
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
        
        # Testes no Servidor Sequencial
        print("\n" + "=" * 50)
        print("SERVIDOR SEQUENCIAL")
        print("=" * 50)
        
        print("\n1. TESTES SEQUENCIAIS GET (25 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteSequencialGET(self.servidor_sequencial_ip, self.porta, 25)
            resultados['servidor_sequencial']['testes_get_sequenciais'].append(metricas)
            time.sleep(1)
        
        print("\n2. TESTES SEQUENCIAIS POST (25 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteSequencialPOST(self.servidor_sequencial_ip, self.porta, 25)
            resultados['servidor_sequencial']['testes_post_sequenciais'].append(metricas)
            time.sleep(1)
        
        print("\n3. TESTES CONCORRENTES GET (5 threads × 10 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteConcorrenteGET(self.servidor_sequencial_ip, self.porta, 5, 10)
            resultados['servidor_sequencial']['testes_get_concorrentes'].append(metricas)
            time.sleep(2)
        
        print("\n4. TESTES CONCORRENTES POST (5 threads × 10 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteConcorrentePOST(self.servidor_sequencial_ip, self.porta, 5, 10)
            resultados['servidor_sequencial']['testes_post_concorrentes'].append(metricas)
            time.sleep(2)
        
        # Testes no Servidor Concorrente
        print("\n" + "=" * 50)
        print("SERVIDOR CONCORRENTE")
        print("=" * 50)
        
        print("\n1. TESTES SEQUENCIAIS GET (25 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteSequencialGET(self.servidor_concorrente_ip, self.porta, 25)
            resultados['servidor_concorrente']['testes_get_sequenciais'].append(metricas)
            time.sleep(1)
        
        print("\n2. TESTES SEQUENCIAIS POST (25 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteSequencialPOST(self.servidor_concorrente_ip, self.porta, 25)
            resultados['servidor_concorrente']['testes_post_sequenciais'].append(metricas)
            time.sleep(1)
        
        print("\n3. TESTES CONCORRENTES GET (5 threads × 10 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteConcorrenteGET(self.servidor_concorrente_ip, self.porta, 5, 10)
            resultados['servidor_concorrente']['testes_get_concorrentes'].append(metricas)
            time.sleep(2)
        
        print("\n4. TESTES CONCORRENTES POST (5 threads × 10 requisições)")
        for i in range(num_execucoes):
            print(f"  Execução {i + 1}/{num_execucoes}...")
            metricas = self.executarTesteConcorrentePOST(self.servidor_concorrente_ip, self.porta, 5, 10)
            resultados['servidor_concorrente']['testes_post_concorrentes'].append(metricas)
            time.sleep(2)
        
        return resultados
    
    def calcularEstatisticasFinais(self, resultados):
        print("\n" + "=" * 70)
        print("ANÁLISE ESTATÍSTICA FINAL - GET E POST (DOCKER)")
        print("=" * 70)
        
        def analisarGrupo(grupo, nome):
            if not grupo:
                return
            
            tempos_medios = [t['tempo_medio'] for t in grupo if t]
            tempos_medianas = [t['tempo_mediana'] for t in grupo if t]
            throughputs = [t['requisicoes_segundo'] for t in grupo if t]
            
            print(f"\n{nome}:")
            print(f"  Tempo Médio:    {statistics.mean(tempos_medios):.4f}s ± {statistics.stdev(tempos_medios):.4f}s")
            print(f"  Tempo Mediana:  {statistics.mean(tempos_medianas):.4f}s ± {statistics.stdev(tempos_medianas):.4f}s")
            print(f"  Throughput:     {statistics.mean(throughputs):.2f} req/s ± {statistics.stdev(throughputs):.2f} req/s")
            print(f"  Taxa de Sucesso: {statistics.mean([t['taxa_sucesso'] for t in grupo]):.1f}%")
        
        print("\n--- SERVIDOR SEQUENCIAL ---")
        analisarGrupo(resultados['servidor_sequencial']['testes_get_sequenciais'], "GET → Sequencial")
        analisarGrupo(resultados['servidor_sequencial']['testes_post_sequenciais'], "POST → Sequencial")
        analisarGrupo(resultados['servidor_sequencial']['testes_get_concorrentes'], "GET → Concorrente")
        analisarGrupo(resultados['servidor_sequencial']['testes_post_concorrentes'], "POST → Concorrente")
        
        print("\n--- SERVIDOR CONCORRENTE ---")
        analisarGrupo(resultados['servidor_concorrente']['testes_get_sequenciais'], "GET → Sequencial")
        analisarGrupo(resultados['servidor_concorrente']['testes_post_sequenciais'], "POST → Sequencial")
        analisarGrupo(resultados['servidor_concorrente']['testes_get_concorrentes'], "GET → Concorrente")
        analisarGrupo(resultados['servidor_concorrente']['testes_post_concorrentes'], "POST → Concorrente")
    
    def salvarResultados(self, resultados):
        import os
        
        try:
            os.makedirs('resultados', exist_ok=True)
            base_path = 'resultados'
        except:
            base_path = '.'
        
        filename = f"{base_path}/metricas_docker_get_post.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados salvos em: {filename}")
        return filename

if __name__ == "__main__":
    print("Iniciando testes completos de métricas DOCKER (GET e POST)...")
    
    testador = TesteMetricas()
    resultados = testador.executarSuiteCompleta(num_execucoes=10)  # 10 execuções conforme pedido
    
    testador.calcularEstatisticasFinais(resultados)
    arquivo_salvo = testador.salvarResultados(resultados)
    
    print("\n" + "=" * 70)
    print("TESTES DOCKER COMPLETOS CONCLUÍDOS!")
    print("=" * 70)
    print(f"Arquivo de resultados: {arquivo_salvo}")
    print("Dados coletados para GET e POST em cenários sequenciais e concorrentes")
    print(f"Servidores testados:")
    print(f"  - Sequencial: {testador.servidor_sequencial_ip}:{testador.porta}")
    print(f"  - Concorrente: {testador.servidor_concorrente_ip}:{testador.porta}")