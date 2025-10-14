import requests
import time
import threading
import statistics
import json
from datetime import datetime

class ClienteTestes:
    def __init__(self, base_url):
        self.base_url = base_url
        self.custom_id = self.calcular_custom_id()
        
    def calcular_custom_id(self):
        import hashlib
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz" 
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def fazer_requisicao_get(self, endpoint="/"):
        """Faz uma requisição GET e mede o tempo"""
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers={'X-Custom-ID': self.custom_id},
                timeout=10
            )
            end_time = time.time()
            
            return {
                'sucesso': True,
                'tempo': end_time - start_time,
                'status_code': response.status_code,
                'custom_id_recebido': response.headers.get('X-Custom-ID', 'Não encontrado')
            }
        except Exception as e:
            end_time = time.time()
            return {
                'sucesso': False,
                'tempo': end_time - start_time,
                'erro': str(e),
                'status_code': None
            }
    
    def fazer_requisicao_post(self, endpoint="/submit", dados="teste"):
        """Faz uma requisição POST e mede o tempo"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                data=dados,
                headers={
                    'X-Custom-ID': self.custom_id,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                timeout=10
            )
            end_time = time.time()
            
            return {
                'sucesso': True,
                'tempo': end_time - start_time,
                'status_code': response.status_code,
                'custom_id_recebido': response.headers.get('X-Custom-ID', 'Não encontrado')
            }
        except Exception as e:
            end_time = time.time()
            return {
                'sucesso': False,
                'tempo': end_time - start_time,
                'erro': str(e),
                'status_code': None
            }
    
    def teste_individual(self, num_requisicoes=10):
        """Teste individual sequencial"""
        print(f"=== TESTE INDIVIDUAL - {self.base_url} ===")
        print(f"Realizando {num_requisicoes} requisições...")
        
        resultados_get = []
        resultados_post = []
        
        # Teste GET
        for i in range(num_requisicoes):
            resultado = self.fazer_requisicao_get()
            resultados_get.append(resultado)
            if resultado['sucesso']:
                print(f"GET {i+1}: {resultado['tempo']:.4f}s - Status: {resultado['status_code']}")
            else:
                print(f"GET {i+1}: ERRO - {resultado['erro']}")
            time.sleep(0.1)
        
        # Teste POST
        for i in range(num_requisicoes):
            resultado = self.fazer_requisicao_post(dados=f"dados_teste_{i}")
            resultados_post.append(resultado)
            if resultado['sucesso']:
                print(f"POST {i+1}: {resultado['tempo']:.4f}s - Status: {resultado['status_code']}")
            else:
                print(f"POST {i+1}: ERRO - {resultado['erro']}")
            time.sleep(0.1)
        
        # Estatísticas
        tempos_get = [r['tempo'] for r in resultados_get if r['sucesso']]
        tempos_post = [r['tempo'] for r in resultados_post if r['sucesso']]
        
        if tempos_get:
            print(f"\n--- ESTATÍSTICAS GET ---")
            print(f"Média: {statistics.mean(tempos_get):.4f}s")
            print(f"Desvio Padrão: {statistics.stdev(tempos_get):.4f}s")
            print(f"Min: {min(tempos_get):.4f}s, Max: {max(tempos_get):.4f}s")
        
        if tempos_post:
            print(f"\n--- ESTATÍSTICAS POST ---")
            print(f"Média: {statistics.mean(tempos_post):.4f}s")
            print(f"Desvio Padrão: {statistics.stdev(tempos_post):.4f}s")
            print(f"Min: {min(tempos_post):.4f}s, Max: {max(tempos_post):.4f}s")
        
        return {
            'get': resultados_get,
            'post': resultados_post,
            'estatisticas_get': {
                'media': statistics.mean(tempos_get) if tempos_get else 0,
                'desvio_padrao': statistics.stdev(tempos_get) if len(tempos_get) > 1 else 0,
                'min': min(tempos_get) if tempos_get else 0,
                'max': max(tempos_get) if tempos_get else 0
            },
            'estatisticas_post': {
                'media': statistics.mean(tempos_post) if tempos_post else 0,
                'desvio_padrao': statistics.stdev(tempos_post) if len(tempos_post) > 1 else 0,
                'min': min(tempos_post) if tempos_post else 0,
                'max': max(tempos_post) if tempos_post else 0
            }
        }

def main():
    # Se utilizarmos localhost, em vez, de docker vai acabar dando erro
    servidores = {
        'sequencial': 'http://servidor-sequencial:80',
        'concorrente': 'http://servidor-concorrente:80'
    }
    
    resultados = {}
    
    for nome, url in servidores.items():
        print(f"\n{'='*50}")
        print(f"TESTANDO SERVIDOR {nome.upper()}")
        print(f"{'='*50}")
        
        cliente = ClienteTestes(url)
        
        # Teste individual
        resultados_individual = cliente.teste_individual(num_requisicoes=5)
        
        resultados[nome] = resultados_individual
        
        time.sleep(2)
    
    # Salvar resultados
    with open('resultados_testes.json', 'w') as f:
        resultados_serializable = {}
        for servidor, dados in resultados.items():
            resultados_serializable[servidor] = {
                'estatisticas_get': dados['estatisticas_get'],
                'estatisticas_post': dados['estatisticas_post']
            }
        json.dump(resultados_serializable, f, indent=2)
    
    print(f"\nResultados salvos em 'resultados_testes.json'")

if __name__ == "__main__":
    main()