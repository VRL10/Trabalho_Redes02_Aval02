import socket
import hashlib
from datetime import datetime
import time
import threading
import json

class ServidorConcorrente:
    def __init__(self,host='37.92.0.11',porta=80):
        self.host = host
        self.porta = porta
        self.id_personalizado = self.calcular_id_personalizado()
        self.contador_requisicoes = 0

        self.lock_contador = threading.Lock() # Trava
        self.semaphore = threading.Semaphore(50) # Limita para 50 thrends
        
    def calcular_id_personalizado(self):
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        
        return hashlib.md5(dados.encode()).hexdigest()
    
    def analisar_requisicao_http(self,dados):
        try:
            linhas = dados.split('\r\n')
            if not linhas:
                return None, None, {}, ''
            
            linha_requisicao = linhas[0]
            partes = linha_requisicao.split()
            if len(partes) < 3:
                return None, None, {}, ''
                
            metodo = partes[0]
            caminho = partes[1]
            
            cabecalhos = {}
            corpo = ''
            linha_vazia_encontrada = False
            
            for linha in linhas[1:]:
                if not linha:
                    linha_vazia_encontrada = True
                    continue
                    
                if not linha_vazia_encontrada and ':' in linha:
                    chave, valor = linha.split(':', 1)
                    cabecalhos[chave.strip()] = valor.strip()
                elif linha_vazia_encontrada:
                    corpo += linha
            
            return metodo, caminho, cabecalhos, corpo.strip()
            
        except Exception as e:
            return None, None, {}, ''
    
    def validar_id_personalizado(self, cabecalhos):
        return cabecalhos.get('X-Custom-ID') == self.id_personalizado
    
    def criar_resposta_http(self, codigo_status, conteudo, tipo_conteudo="text/html", cabecalhos_personalizados=None):
        mensagens_status = {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        
        resposta = f"HTTP/1.1 {codigo_status} {mensagens_status.get(codigo_status, 'Unknown')}\r\n"
        resposta += f"Content-Type: {tipo_conteudo}; charset=utf-8\r\n"
        resposta += f"X-Custom-ID: {self.id_personalizado}\r\n"
        resposta += f"Server: Concorrente-Socket/Redes-II\r\n"
        resposta += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        resposta += f"Content-Length: {len(conteudo.encode('utf-8'))}\r\n"
        resposta += "Connection: close\r\n"
        
        if cabecalhos_personalizados:
            for chave, valor in cabecalhos_personalizados.items():
                resposta += f"{chave}: {valor}\r\n"
        
        resposta += "\r\n"
        resposta += conteudo
        
        return resposta
    
    def processar_requisicao_get(self,caminho, cabecalhos):
        if not self.validar_id_personalizado(cabecalhos):
            return self.criar_resposta_http(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>")
        
        with self.lock_contador:
            self.contador_requisicoes += 1
            contador_atual = self.contador_requisicoes
        
        if caminho == '/' or caminho == '/index.html':
            conteudo = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Servidor Concorrente - Sockets</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Servidor Web Concorrente com Sockets Brutos</h1>
    <p><strong>Matrícula:</strong> 20229043792</p>
    <p><strong>Nome:</strong> Victor Rodrigues Luz</p>
    <p><strong>Thread:</strong> {threading.current_thread().name}</p>
    <p><strong>Requisição nº:</strong> {contador_atual}</p>
    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>X-Custom-ID:</strong> {self.id_personalizado}</p>
    <p><strong>Tipo:</strong> Concorrente (Socket TCP + Threads)</p>
</body>
</html>
"""
            return self.criar_resposta_http(200, conteudo, "text/html")
            
        elif caminho == '/info':
            info = {
                "servidor": "concorrente_socket",
                "matricula": "20229043792",
                "nome": "Victor Rodrigues Luz",
                "thread": threading.current_thread().name,
                "custom_id": self.id_personalizado,
                "timestamp": datetime.now().isoformat(),
                "request_count": contador_atual,
                "protocol": "TCP/Socket",
                "concurrency": "thread-based"
            }
            return self.criar_resposta_http(200, json.dumps(info, indent=2), "application/json")
            
        elif caminho == '/status':
            status_info = {
                "status":"online",
                "server_type":"concurrent",
                "requests_processed":contador_atual,
                "active_threads":threading.active_count(),
                "thread_name":threading.current_thread().name,
                "custom_id_valid": True
            }
            return self.criar_resposta_http(200, json.dumps(status_info, indent=2), "application/json")
            
        elif caminho == '/heavy':
            time.sleep(2)
            conteudo = {
                "operation": "heavy_processing",
                "duration": "2 seconds",
                "thread": threading.current_thread().name,
                "timestamp": datetime.now().isoformat()
            }
            return self.criar_resposta_http(200, json.dumps(conteudo, indent=2), "application/json")

        elif caminho == '/health':
            health_info = {
                "status": "healthy", 
                "server": "concorrente",
                "threads_ativas": threading.active_count(),
                "timestamp": datetime.now().isoformat()
            }
            return self.criar_resposta_http(200, json.dumps(health_info, indent=2), "application/json")

        else:
            return self.criar_resposta_http(404,"<h1>404 - Recurso Não Encontrado</h1><p>Use: /, /info, /status, /heavy, /health</p>")
    
    def processar_requisicao_post(self, caminho,cabecalhos, corpo):
        if not self.validar_id_personalizado(cabecalhos):
            return self.criar_resposta_http(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>")
        
        with self.lock_contador:
            self.contador_requisicoes += 1
            contador_atual = self.contador_requisicoes
        
        if caminho == '/api/data':
            tempo_processamento = 0.1
            time.sleep(tempo_processamento)
            
            dados_resposta = {
                "status": "processed",
                "data_received": corpo,
                "data_length": len(corpo),
                "processing_time": f"{tempo_processamento}s",
                "processed_at": datetime.now().isoformat(),
                "request_id": contador_atual,
                "thread": threading.current_thread().name,
                "custom_id": self.id_personalizado
            }
            return self.criar_resposta_http(200, json.dumps(dados_resposta,indent=2), "application/json")
            
        elif caminho == '/api/echo':
            resposta_echo = {
                "echo": corpo,
                "timestamp": datetime.now().isoformat(),
                "received_bytes": len(corpo),
                "thread": threading.current_thread().name
            }
            return self.criar_resposta_http(200, json.dumps(resposta_echo,indent=2), "application/json")
            
        elif caminho == '/api/batch':
            time.sleep(0.5)
            resposta_lote = {
                "operation": "batch_processing",
                "items_processed": len(corpo.split(',')),
                "processing_time": "0.5s",
                "thread": threading.current_thread().name,
                "timestamp": datetime.now().isoformat()
            }
            return self.criar_resposta_http(200, json.dumps(resposta_lote, indent=2), "application/json")
            
        else:
            return self.criar_resposta_http(404, "<h1>404 - Endpoint POST não encontrado</h1>")
    
    def processar_cliente(self,socket_cliente,endereco_cliente):
        with self.semaphore:
            nome_thread = threading.current_thread().name
            tempo_inicio = time.time()
            
            try:
                dados_requisicao = b""
                socket_cliente.settimeout(10.0)
                
                while True:
                    pedaco = socket_cliente.recv(1024)
                    if not pedaco:
                        break
                    dados_requisicao += pedaco
                    if b'\r\n\r\n' in dados_requisicao:
                        break
                
                if not dados_requisicao:
                    return
                
                texto_requisicao = dados_requisicao.decode('utf-8',errors='ignore')
                metodo, caminho, cabecalhos, corpo = self.analisar_requisicao_http(texto_requisicao)
                
                print(f"[{nome_thread}] {endereco_cliente} - {metodo} {caminho}")
                
                if metodo == 'GET':
                    resposta = self.processar_requisicao_get(caminho, cabecalhos)
                elif metodo == 'POST':
                    resposta = self.processar_requisicao_post(caminho, cabecalhos, corpo)
                elif metodo == 'HEAD':
                    if caminho == '/':
                        resposta = self.criar_resposta_http(200, "", "text/html")
                    else:
                        resposta = self.criar_resposta_http(404, "")
                else:
                    resposta = self.criar_resposta_http(405, "<h1>405 - Método Não Permitido</h1>")
                
                socket_cliente.send(resposta.encode('utf-8'))
                
                tempo_processamento = time.time() - tempo_inicio
                print(f"[{nome_thread}] Resposta enviada em {tempo_processamento:.3f}s")
                
            except socket.timeout:
                resposta_erro = self.criar_resposta_http(408, "<h1>408 - Timeout</h1>")
                socket_cliente.send(resposta_erro.encode('utf-8'))
                print(f"[{nome_thread}] Timeout com {endereco_cliente}")
            except Exception as e:
                resposta_erro = self.criar_resposta_http(500, f"<h1>500 - Erro Interno</h1><p>{str(e)}</p>")
                socket_cliente.send(resposta_erro.encode('utf-8'))
                print(f"[{nome_thread}] Erro: {e}")
            finally:
                socket_cliente.close()
                print(f"[{nome_thread}] Conexao fechada: {endereco_cliente}")
    
    def iniciar(self):
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_servidor.bind((self.host, self.porta))
        socket_servidor.listen(10)
        
        print("=" * 70)
        print("SERVIDOR CONCORRENTE - SOCKETS BRUTOS")
        print("=" * 70)
        print(f"Servidor: {self.host}:{self.porta}")
        print(f"X-Custom-ID: {self.id_personalizado}")
        print(f"MATRicula:20229043792")
        print(f"Nome: Victor Rodrigues Luz")
        print("Endpoints: GET /, /info, /status, /heavy, /health")
        print("Endpoints: POST /api/data, /api/echo, /api/batch")
        print("Digite Ctrl+C para encerrar")
        print("=" * 70)
        
        try:
            while True:
                socket_cliente, endereco_cliente = socket_servidor.accept()
                print(f"\n[Main] Conexao aceita: {endereco_cliente}")
                
                thread_cliente = threading.Thread(
                    target=self.processar_cliente,
                    args=(socket_cliente, endereco_cliente),
                    name=f"Thread-{threading.active_count()}"
                )
                thread_cliente.daemon = True
                thread_cliente.start()
                
                print(f"[Main] Thread iniciada: {thread_cliente.name}")
                print(f"[Main] Threads ativas: {threading.active_count() - 1}")
                
        except KeyboardInterrupt:
            print("\n[Main] Encerrando servidor...")
        except Exception as e:
            print(f"\n[Main] Erro: {e}")
        finally:
            socket_servidor.close()

if __name__ == "__main__":
    servidor = ServidorConcorrente()
    servidor.iniciar()