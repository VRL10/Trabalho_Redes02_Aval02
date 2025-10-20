"""
Cliente de Testes para Servidores Web - Redes de Computadores II
Autor: Victor Rodrigues Luz - Matricula: 20229043792
"""

import socket
import time
import statistics
import threading
import hashlib
import json
from datetime import datetime

class ClienteTestes:
    def __init__(self, serverHost, serverPort=80):
        """
        Inicializa o cliente de testes com sockets TCP puros
        
        Args:
            serverHost (str): IP do servidor (ex: '37.92.00.10')
            serverPort (int): Porta do servidor
        """
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.customID = self.calcularCustomID()
        
    def calcularCustomID(self):
        """Calcula o X-Custom-ID igual aos servidores"""
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def criarRequisicaoHTTP(self, method="GET", path="/", body=""):
        """
        Cria uma requisicao HTTP valida com X-Custom-ID
        
        Returns:
            str: Requisicao HTTP formatada
        """
        requisicao = f"""{method} {path} HTTP/1.1
Host: {self.serverHost}:{self.serverPort}
X-Custom-ID: {self.customID}
User-Agent: Cliente-Testes-Redes-II
Accept: text/html,application/json
Connection: close
Content-Length: {len(body)}

{body}"""
        
        return requisicao.replace('\n', '\r\n')
    
    def enviarRequisicao(self, requisicaoHTTP):
        """
        Envia requisicao via socket e mede tempo de resposta
        
        Returns:
            tuple: (tempoResposta, statusCode, sucesso)
        """
        startTime = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.serverHost, self.serverPort))
            sock.sendall(requisicaoHTTP.encode('utf-8'))
            
            resposta = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                resposta += data
            
            tempoResposta = time.time() - startTime
            
            respostaStr = resposta.decode('utf-8')
            linhas = respostaStr.split('\r\n')
            statusCode = 0
            if linhas and 'HTTP' in linhas[0]:
                statusCode = int(linhas[0].split(' ')[1])
            
            sock.close()
            return tempoResposta, statusCode, True
            
        except Exception as e:
            tempoResposta = time.time() - startTime
            return tempoResposta, 0, False
    
    def testeIndividual(self, numRequisicoes=10):
        """
        Executa teste individual sequencial
        
        Returns:
            dict: Estatisticas do teste
        """
        print(f"Executando teste individual com {numRequisicoes} requisicoes...")
        
        tempos = []
        sucessos = 0
        falhas = 0
        
        for i in range(numRequisicoes):
            requisicao = self.criarRequisicaoHTTP("GET", "/")
            tempo, status, sucesso = self.enviarRequisicao(requisicao)
            
            tempos.append(tempo)
            if sucesso and status == 200:
                sucessos += 1
            else:
                falhas += 1
            
            print(f"Requisicao {i+1}: {tempo:.4f}s - Status: {status}")
            time.sleep(0.1)
        
        if tempos:
            estatisticas = {
                'totalRequisicoes': numRequisicoes,
                'sucessos': sucessos,
                'falhas': falhas,
                'taxaSucesso': (sucessos / numRequisicoes) * 100,
                'tempoMedio': statistics.mean(tempos),
                'tempoMinimo': min(tempos),
                'tempoMaximo': max(tempos),
                'desvioPadrao': statistics.stdev(tempos) if len(tempos) > 1 else 0,
                'throughput': numRequisicoes / sum(tempos) if sum(tempos) > 0 else 0
            }
        else:
            estatisticas = {}
        
        return estatisticas
    
    def testeConcorrente(self, numThreads=5, requisicoesPorThread=10):
        """
        Executa teste com multiplas threads simulando carga concorrente
        
        Returns:
            dict: Estatisticas do teste concorrente
        """
        print(f"Executando teste concorrente: {numThreads} threads, {requisicoesPorThread} req/thread")
        
        resultados = {
            'tempos': [],
            'sucessos': 0,
            'falhas': 0,
            'lock': threading.Lock()
        }
        
        def workerThread(threadId):
            for i in range(requisicoesPorThread):
                requisicao = self.criarRequisicaoHTTP("GET", "/")
                tempo, status, sucesso = self.enviarRequisicao(requisicao)
                
                with resultados['lock']:
                    resultados['tempos'].append(tempo)
                    if sucesso and status == 200:
                        resultados['sucessos'] += 1
                    else:
                        resultados['falhas'] += 1
                
                print(f"Thread {threadId}, Req {i+1}: {tempo:.4f}s")
        
        threads = []
        startTime = time.time()
        
        for i in range(numThreads):
            thread = threading.Thread(target=workerThread, args=(i+1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tempoTotal = time.time() - startTime
        totalRequisicoes = numThreads * requisicoesPorThread
        
        if resultados['tempos']:
            estatisticas = {
                'totalRequisicoes': totalRequisicoes,
                'threads': numThreads,
                'requisicoesPorThread': requisicoesPorThread,
                'sucessos': resultados['sucessos'],
                'falhas': resultados['falhas'],
                'taxaSucesso': (resultados['sucessos'] / totalRequisicoes) * 100,
                'tempoTotalTeste': tempoTotal,
                'tempoMedio': statistics.mean(resultados['tempos']),
                'tempoMinimo': min(resultados['tempos']),
                'tempoMaximo': max(resultados['tempos']),
                'desvioPadrao': statistics.stdev(resultados['tempos']) if len(resultados['tempos']) > 1 else 0,
                'throughput': totalRequisicoes / tempoTotal
            }
        else:
            estatisticas = {}
        
        return estatisticas
    
    def executarSuiteTestes(self, numExecucoes=10):
        """
        Executa suite completa de testes para analise estatistica
        
        Returns:
            dict: Resultados completos dos testes
        """
        print("=" * 60)
        print("SUITE DE TESTES - REDES DE COMPUTADORES II")
        print("=" * 60)
        print(f"Servidor: {self.serverHost}:{self.serverPort}")
        print(f"X-Custom-ID: {self.customID}")
        print(f"Execucoes: {numExecucoes}")
        print("=" * 60)
        
        resultados = {
            'testesSequenciais': [],
            'testesConcorrentes': [],
            'metadata': {
                'servidor': self.serverHost,
                'porta': self.serverPort,
                'customID': self.customID,
                'dataTestes': datetime.now().isoformat(),
                'matricula': '20229043792',
                'nome': 'Victor Rodrigues Luz'
            }
        }
        
        print("\n1. TESTES SEQUENCIAIS")
        for i in range(numExecucoes):
            print(f"\nExecucao {i+1}/{numExecucoes}:")
            stats = self.testeIndividual(numRequisicoes=10)
            resultados['testesSequenciais'].append(stats)
            time.sleep(1)
        
        print("\n2. TESTES CONCORRENTES")
        for i in range(numExecucoes):
            print(f"\nExecucao {i+1}/{numExecucoes}:")
            stats = self.testeConcorrente(numThreads=5, requisicoesPorThread=10)
            resultados['testesConcorrentes'].append(stats)
            time.sleep(2)
        
        return resultados
    
    def gerarRelatorio(self, resultados):
        """Gera relatorio resumido dos testes"""
        print("\n" + "=" * 60)
        print("RELATORIO DE TESTES")
        print("=" * 60)
        
        seqTempos = [t['tempoMedio'] for t in resultados['testesSequenciais'] if t]
        concTempos = [t['tempoMedio'] for t in resultados['testesConcorrentes'] if t]
        
        if seqTempos:
            print("\nSEQUENCIAL - Estatisticas (10 execucoes):")
            print(f"  Tempo medio: {statistics.mean(seqTempos):.4f}s")
            print(f"  Desvio padrao: {statistics.stdev(seqTempos):.4f}s")
            print(f"  Throughput medio: {statistics.mean([t['throughput'] for t in resultados['testesSequenciais']]):.2f} req/s")
        
        if concTempos:
            print("\nCONCORRENTE - Estatisticas (10 execucoes):")
            print(f"  Tempo medio: {statistics.mean(concTempos):.4f}s")
            print(f"  Desvio padrao: {statistics.stdev(concTempos):.4f}s")
            print(f"  Throughput medio: {statistics.mean([t['throughput'] for t in resultados['testesConcorrentes']]):.2f} req/s")
        
        with open('resultadosTestes.json', 'w') as f:
            json.dump(resultados, f, indent=2)
        
        print(f"\nResultados salvos em 'resultadosTestes.json'")

if __name__ == "__main__":
    # Testa AMBOS os servidores
    print("=== TESTANDO SERVIDOR SEQUENCIAL ===")
    cliente_seq = ClienteTestes('43.79.0.10', 80)  # IP Docker
    resultados_seq = cliente_seq.executarSuiteTestes(numExecucoes=10)
    cliente_seq.gerarRelatorio(resultados_seq)
    
    print("\n=== TESTANDO SERVIDOR CONCORRENTE ===")
    cliente_conc = ClienteTestes('43.79.0.11', 80)  # IP Docker
    resultados_conc = cliente_conc.executarSuiteTestes(numExecucoes=10)
    cliente_conc.gerarRelatorio(resultados_conc)