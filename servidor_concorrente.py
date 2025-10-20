import socket
import hashlib
from datetime import datetime
import json
import threading
import time

class ServidorConcorrente:
    """
    Servidor Web Concorrente implementado com sockets TCP e threads
    Atende requisições HTTP na porta 8080
    """
    
    def __init__(self, host='0.0.0.0', port=80):
        """
        Inicializa o servidor concorrente
        
        Args:
            host (str): Endereço IP do servidor
            port (int): Porta do servidor
        """
        self.host = host
        self.port = port
        self.custom_id = self.calcular_custom_id()
        self.lock = threading.Lock()
        self.request_count = 0  # Contador de requisições para métricas
        
    def calcular_custom_id(self):
        """
        Calcula o X-Custom-ID baseado na matrícula e nome conforme especificado
        Usa MD5 conforme permitido no trabalho
        
        Returns:
            str: Hash MD5 dos dados
        """
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def parse_http_request(self, data):
        """
        Faz parsing da requisição HTTP conforme protocolo
        
        Args:
            data (str): Dados brutos da requisição
            
        Returns:
            tuple: (method, path, headers, body)
        """
        if not data:
            return None, None, {}, ''
            
        lines = data.split('\r\n')
        if not lines:
            return None, None, {}, ''
        
        # Parse da linha de requisição
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) < 2:
            return None, None, {}, ''
        
        method = parts[0]
        path = parts[1]
        
        # Parse dos headers
        headers = {}
        body_start = False
        for i, line in enumerate(lines[1:], 1):
            if line == '':
                body_start = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        # Parse do body
        body = ''
        if body_start and body_start < len(lines):
            body = '\r\n'.join(lines[body_start:])
        
        return method, path, headers, body
    
    def validar_custom_id(self, headers):
        """
        Valida o cabeçalho X-Custom-ID obrigatório
        
        Args:
            headers (dict): Headers da requisição
            
        Returns:
            bool: True se válido, False caso contrário
        """
        custom_id = headers.get('X-Custom-ID', '')
        return custom_id == self.custom_id
    
    def handle_get(self, path, headers):
        """
        Processa requisições GET conforme especificado no trabalho
        
        Args:
            path (str): Caminho da requisição
            headers (dict): Headers da requisição
            
        Returns:
            str: Resposta HTTP formatada
        """
        # Validação do Custom-ID
        if not self.validar_custom_id(headers):
            return self.error_400("X-Custom-ID inválido ou ausente")
        
        # Incrementa contador de requisições de forma thread-safe
        with self.lock:
            self.request_count += 1
            current_count = self.request_count
        
        if path == '/':
            # Página principal
            response_body = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Servidor Concorrente - Redes II</title>
                    <meta charset="utf-8">
                </head>
                <body>
                    <h1>Servidor Web Concorrente</h1>
                    <p><strong>Matrícula:</strong> 20229043792</p>
                    <p><strong>Nome:</strong> Victor Rodrigues Luz</p>
                    <p><strong>Thread:</strong> {threading.current_thread().name}</p>
                    <p><strong>Requisição nº:</strong> {current_count}</p>
                    <p><strong>Hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>X-Custom-ID:</strong> {self.custom_id}</p>
                    
                    <h2>Testar Métodos:</h2>
                    <ul>
                        <li><a href="/info">GET /info (JSON)</a></li>
                        <li><a href="/stats">GET /stats (Estatísticas)</a></li>
                    </ul>
                    
                    <h2>Formulário POST:</h2>
                    <form method="POST" action="/submit">
                        <input type="text" name="dados" placeholder="Digite algo para testar POST" required>
                        <button type="submit">Enviar via POST</button>
                    </form>
                </body>
            </html>
            """
            content_type = "text/html; charset=utf-8"
            
        elif path == '/info':
            # Endpoint de informações em JSON
            response_body = json.dumps({
                "servidor": "concorrente",
                "matricula": "20229043792",
                "nome": "Victor Rodrigues Luz",
                "thread": threading.current_thread().name,
                "custom_id": self.custom_id,
                "timestamp": datetime.now().isoformat(),
                "request_count": current_count
            }, indent=2)
            content_type = "application/json"
            
        elif path == '/stats':
            # Endpoint de estatísticas
            response_body = json.dumps({
                "total_requests": current_count,
                "server_type": "concorrente",
                "active_threads": threading.active_count(),
                "timestamp": datetime.now().isoformat(),
                "custom_id": self.custom_id
            }, indent=2)
            content_type = "application/json"
            
        else:
            return self.error_404()
        
        # Construção da resposta HTTP
        response = f"""HTTP/1.1 200 OK
Content-Type: {content_type}
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{response_body}"""
        return response
    
    def handle_post(self, path, headers, body):
        """
        Processa requisições POST conforme especificado no trabalho
        
        Args:
            path (str): Caminho da requisição
            headers (dict): Headers da requisição
            body (str): Corpo da requisição
            
        Returns:
            str: Resposta HTTP formatada
        """
        # Validação do Custom-ID
        if not self.validar_custom_id(headers):
            return self.error_400("X-Custom-ID inválido ou ausente")
        
        if path == '/submit':
            # Processa submissão de formulário
            response_body = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Dados Recebidos - Concorrente</title>
                    <meta charset="utf-8">
                </head>
                <body>
                    <h1>Dados Recebidos - Servidor Concorrente</h1>
                    <p><strong>Conteúdo recebido:</strong> {body}</p>
                    <p><strong>Thread:</strong> {threading.current_thread().name}</p>
                    <p><strong>Custom-ID:</strong> {self.custom_id}</p>
                    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <a href="/">Voltar para página inicial</a>
                </body>
            </html>
            """
            
            response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{response_body}"""
            return response
        else:
            return self.error_404()
    
    def error_400(self, message="Requisição Inválida"):
        """Retorna erro 400 Bad Request"""
        response_body = f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h1>400 - Bad Request</h1>
                <p>{message}</p>
                <p>X-Custom-ID é obrigatório e deve ser válido</p>
            </body>
        </html>
        """
        
        response = f"""HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II

{response_body}"""
        return response
    
    def error_404(self):
        """Retorna erro 404 Not Found"""
        response_body = """
        <!DOCTYPE html>
        <html>
            <body>
                <h1>404 - Página Não Encontrada</h1>
                <p>Recurso solicitado não existe neste servidor</p>
                <a href="/">Voltar para página inicial</a>
            </body>
        </html>
        """
        
        response = f"""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II

{response_body}"""
        return response
    
    def error_405(self):
        """Retorna erro 405 Method Not Allowed"""
        response_body = """
        <!DOCTYPE html>
        <html>
            <body>
                <h1>405 - Método Não Permitido</h1>
                <p>Método HTTP não suportado para este recurso</p>
            </body>
        </html>
        """
        
        response = f"""HTTP/1.1 405 Method Not Allowed
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II

{response_body}"""
        return response
    
    def handle_client(self, client_socket, addr):
        """
        Processa um cliente em thread separada
        Implementa o modelo concorrente com threads
        
        Args:
            client_socket (socket): Socket do cliente
            addr (tuple): Endereço do cliente
        """
        start_time = time.time()
        thread_name = threading.current_thread().name
        
        try:
            # Recebe dados do cliente
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return
            
            print(f"[{thread_name}] Requisição de {addr}")
            print(f"[{thread_name}] Dados recebidos:\n{data[:500]}...")
            
            # Parse da requisição HTTP
            method, path, headers, body = self.parse_http_request(data)
            
            print(f"[{thread_name}] Método: {method}, Path: {path}")
            
            # Processa conforme o método HTTP
            if method == 'GET':
                response = self.handle_get(path, headers)
            elif method == 'POST':
                response = self.handle_post(path, headers, body)
            else:
                response = self.error_405()
            
            # Envia resposta
            client_socket.sendall(response.encode('utf-8'))
            
            # Log de métricas
            processing_time = time.time() - start_time
            print(f"[{thread_name}] Resposta enviada em {processing_time:.4f}s")
            
        except Exception as e:
            # Tratamento de erro genérico
            error_response = f"""HTTP/1.1 500 Internal Server Error
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python/Redes-II

<html>
<body>
    <h1>500 - Erro Interno do Servidor</h1>
    <p>{str(e)}</p>
</body>
</html>"""
            client_socket.sendall(error_response.encode('utf-8'))
            print(f"[{thread_name}] Erro: {str(e)}")
            
        finally:
            # Fecha conexão com cliente
            client_socket.close()
            print(f"[{thread_name}] Conexão com {addr} fechada")
    
    def iniciar(self):
        """
        Inicia o servidor concorrente
        Fica ouvindo na porta especificada e cria threads para cada cliente
        """
        # Cria socket TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)  # Fila de 10 conexões
        
        print("=" * 60)
        print("SERVIDOR CONCORRENTE - REDES DE COMPUTADORES II")
        print("=" * 60)
        print(f"Servidor rodando em: {self.host}:{self.port}")
        print(f"X-Custom-ID: {self.custom_id}")
        print(f"Matrícula: 20229043792")
        print(f"Nome: Victor Rodrigues Luz")
        print("Pressione Ctrl+C para encerrar o servidor")
        print("=" * 60)
        
        try:
            while True:
                # Aguarda conexões
                client_socket, addr = server_socket.accept()
                print(f"\n[Main] Conexão aceita de {addr}")
                
                # Cria nova thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    name=f"Thread-{threading.active_count()}"
                )
                client_thread.daemon = True
                client_thread.start()
                
                print(f"[Main] Thread {client_thread.name} iniciada para {addr}")
                print(f"[Main] Threads ativas: {threading.active_count() - 1}")
                
        except KeyboardInterrupt:
            print("\n[Main] Encerrando servidor...")
        except Exception as e:
            print(f"\n[Main] Erro no servidor: {str(e)}")
        finally:
            server_socket.close()
            print("[Main] Socket do servidor fechado")

if __name__ == "__main__":
    # Inicia o servidor concorrente
    servidor = ServidorConcorrente()
    servidor.iniciar()