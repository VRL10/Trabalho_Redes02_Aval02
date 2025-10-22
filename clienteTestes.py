import socket
import time
import statistics
import threading
import hashlib
import json
from datetime import datetime

class ClienteTestes:
    def __init__(self):
        self.idCustom = hashlib.md5("20229043792 Victor Rodrigues Luz".encode()).hexdigest()
    
    def criarRequisicaoHTTP(self, metodo="GET", caminho="/", corpo=""):
        if metodo == "GET":
            requisicao = f"""GET {caminho} HTTP/1.1\r
Host: 37.92.0.10\r
X-Custom-ID: {self.idCustom}\r
User-Agent: Cliente-Teste-Sockets/Redes-II\r
Connection: close\r
\r
"""
        else:
            requisicao = f"""POST {caminho} HTTP/1.1\r
Host: 37.92.0.10\r
X-Custom-ID: {self.idCustom}\r
User-Agent: Cliente-Teste-Sockets/Redes-II\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {len(corpo)}\r
Connection: close\r
\r
{corpo}"""
        
        return requisicao
    
    def medirRequisicao(self, ip, porta, metodo, caminho, corpo=""):
        inicio = time.time()
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((ip, porta))
            
            requisicao = self.criarRequisicaoHTTP(metodo, caminho, corpo)
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
            return time.time() - inicio, 0, False
    
    def executarTesteSequencial(self, ip, porta, metodo, num_requisicoes=25):
        print(f"Teste SEQUENCIAL {metodo}: {ip}:{porta} - {num_requisicoes} requisições")
        
        tempos = []
        sucessos = 0
        inicio_teste = time.time()
        
        for i in range(num_requisicoes):
            if metodo == "GET":
                caminho = "/info" if i % 3 == 0 else "/"
                corpo = ""
            else:
                caminho = "/api/data"
                corpo = f"dados=teste_{i}_valor_{i*2}"
            
            tempo, status, sucesso = self.medirRequisicao(ip, porta, metodo, caminho, corpo)
            
            tempos.append(tempo)
            if sucesso:
                sucessos += 1
            
            if (i + 1) % 10 == 0:
                print(f"  {metodo} Concluídas: {i + 1}/{num_requisicoes}")
        
        tempo_total = time.time() - inicio_teste
        
        return {
            'metodo': metodo,
            'cenario': 'sequencial',
            'total_requisicoes': num_requisicoes,
            'sucessos': sucessos,
            'falhas': num_requisicoes - sucessos,
            'taxa_sucesso': (sucessos / num_requisicoes) * 100,
            'tempo_total': tempo_total,
            'tempo_medio': statistics.mean(tempos),
            'tempo_minimo': min(tempos),
            'tempo_maximo': max(tempos),
            'desvio_padrao': statistics.stdev(tempos) if len(tempos) > 1 else 0,
            'throughput': num_requisicoes / tempo_total
        }
    
    def executarTesteConcorrente(self, ip, porta, metodo, num_threads=5, requisicoes_por_thread=10):
        print(f"Teste CONCORRENTE {metodo}: {ip}:{porta} - {num_threads} threads × {requisicoes_por_thread} reqs")
        
        resultados = {
            'tempos': [],
            'sucessos': 0,
            'lock': threading.Lock()
        }
        
        def worker_thread(thread_id):
            for i in range(requisicoes_por_thread):
                if metodo == "GET":
                    if i % 4 == 0:
                        caminho = "/heavy"
                    elif i % 3 == 0:
                        caminho = "/status"
                    elif i % 2 == 0:
                        caminho = "/info"
                    else:
                        caminho = "/"
                    corpo = ""
                else:
                    if i % 3 == 0:
                        caminho = "/api/batch"
                        corpo = f"item_{i},item_{i+1},item_{i+2}"
                    elif i % 2 == 0:
                        caminho = "/api/echo"
                        corpo = f"dados_thread_{thread_id}_req_{i}"
                    else:
                        caminho = "/api/data"
                        corpo = f"dados=thread_{thread_id}_req_{i}"
                
                tempo, status, sucesso = self.medirRequisicao(ip, porta, metodo, caminho, corpo)
                
                with resultados['lock']:
                    resultados['tempos'].append(tempo)
                    if sucesso:
                        resultados['sucessos'] += 1
        
        threads = []
        inicio_teste = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(i + 1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tempo_total = time.time() - inicio_teste
        total_requisicoes = num_threads * requisicoes_por_thread
        
        return {
            'metodo': metodo,
            'cenario': 'concorrente',
            'total_requisicoes': total_requisicoes,
            'threads': num_threads,
            'requisicoes_por_thread': requisicoes_por_thread,
            'sucessos': resultados['sucessos'],
            'falhas': total_requisicoes - resultados['sucessos'],
            'taxa_sucesso': (resultados['sucessos'] / total_requisicoes) * 100,
            'tempo_total': tempo_total,
            'tempo_medio': statistics.mean(resultados['tempos']),
            'tempo_minimo': min(resultados['tempos']),
            'tempo_maximo': max(resultados['tempos']),
            'desvio_padrao': statistics.stdev(resultados['tempos']) if len(resultados['tempos']) > 1 else 0,
            'throughput': total_requisicoes / tempo_total
        }
    
    def executarSuiteCompleta(self, num_execucoes=10):
        print("=" * 70)
        print("SUITE COMPLETA DE TESTES - SOCKETS BRUTOS")
        print("=" * 70)
        print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Execuções por teste: {num_execucoes}")
        print(f"X-Custom-ID: {self.idCustom}")
        print("Servidor Sequencial: 37.92.0.10:80")
        print("Servidor Concorrente: 37.92.0.11:80")
        print("=" * 70)
        
        resultados = {
            'metadata': {
                'matricula': '20229043792',
                'nome': 'Victor Rodrigues Luz',
                'data_testes': datetime.now().isoformat(),
                'num_execucoes': num_execucoes,
                'custom_id': self.idCustom,
                'subrede': '37.92.0.0/16',
                'protocolo': 'TCP/Sockets-Brutos',
                'metricas_coletadas': [
                    'Tempo de Resposta (s)',
                    'Throughput (req/s)', 
                    'Taxa de Sucesso (%)',
                    'Desvio Padrão (consistência)',
                    'Latência Mínima/Máxima'
                ]
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
        
        print("\n" + "=" * 50)
        print("SERVIDOR SEQUENCIAL")
        print("=" * 50)
        
        for i in range(num_execucoes):
            print(f"\nExecução {i+1}/{num_execucoes}")
            
            resultados['servidor_sequencial']['testes_get_sequenciais'].append(
                self.executarTesteSequencial('37.92.0.10', 80, 'GET', 25)
            )
            time.sleep(1)
            
            resultados['servidor_sequencial']['testes_post_sequenciais'].append(
                self.executarTesteSequencial('37.92.0.10', 80, 'POST', 25)
            )
            time.sleep(1)
            
            resultados['servidor_sequencial']['testes_get_concorrentes'].append(
                self.executarTesteConcorrente('37.92.0.10', 80, 'GET', 5, 10)
            )
            time.sleep(2)
            
            resultados['servidor_sequencial']['testes_post_concorrentes'].append(
                self.executarTesteConcorrente('37.92.0.10', 80, 'POST', 5, 10)
            )
            time.sleep(2)
        
        print("\n" + "=" * 50)
        print("SERVIDOR CONCORRENTE")
        print("=" * 50)
        
        for i in range(num_execucoes):
            print(f"\nExecução {i+1}/{num_execucoes}")
            
            resultados['servidor_concorrente']['testes_get_sequenciais'].append(
                self.executarTesteSequencial('37.92.0.11', 80, 'GET', 25)
            )
            time.sleep(1)
            
            resultados['servidor_concorrente']['testes_post_sequenciais'].append(
                self.executarTesteSequencial('37.92.0.11', 80, 'POST', 25)
            )
            time.sleep(1)
            
            resultados['servidor_concorrente']['testes_get_concorrentes'].append(
                self.executarTesteConcorrente('37.92.0.11', 80, 'GET', 5, 10)
            )
            time.sleep(2)
            
            resultados['servidor_concorrente']['testes_post_concorrentes'].append(
                self.executarTesteConcorrente('37.92.0.11', 80, 'POST', 5, 10)
            )
            time.sleep(2)
        
        with open('/app/resultados/metricas_completas.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        return resultados

if __name__ == "__main__":
    cliente = ClienteTestes()
    resultados = cliente.executarSuiteCompleta(num_execucoes=10)
    
    print("\n" + "=" * 70)
    print("SUITE DE TESTES CONCLUÍDA!")
    print("=" * 70)
    print("Resultados salvos em: /app/resultados/metricas_completas.json")