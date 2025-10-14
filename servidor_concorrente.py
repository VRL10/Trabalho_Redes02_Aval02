import socket
import hashlib
from datetime import datetime
import json
import threading

class ServidorConcorrente:
    def __init__(self, host='0.0.0.0', port=80):
        self.host = host
        self.port = port
        self.custom_id = self.calcular_custom_id()
        self.lock = threading.Lock()
        
    def calcular_custom_id(self):
        """Calcula o X-Custom-ID baseado na matrícula e nome"""
        matricula = "20229043792"
        nome = "SEU_NOME_COMPLETO"  # ALTERE AQUI!
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def parse_http_request(self, data):
        """Faz parsing básico da requisição HTTP"""
        lines = data.split('\r\n')
        if not lines:
            return None, None, {}
        
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) < 2:
            return None, None, {}
        
        method = parts[0]
        path = parts[1]
        
        headers = {}
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
            elif line == '':
                break
        
        body = ''
        if '\r\n\r\n' in data:
            body = data.split('\r\n\r\n')[1]
        
        return method, path, headers, body
    
    def handle_get(self, path, headers):
        """Processa requisições GET"""
        if path == '/':
            response_body = f"""
            <html>
                <head><title>Servidor Concorrente</title></head>
                <body>
                    <h1>Servidor Web Concorrente</h1>
                    <p>Matrícula: 20229043792</p>
                    <p>Thread: {threading.current_thread().name}</p>
                    <p>Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <form method="POST" action="/submit">
                        <input type="text" name="dados" placeholder="Digite algo">
                        <button type="submit">Enviar</button>
                    </form>
                </body>
            </html>
            """
        elif path == '/info':
            response_body = json.dumps({
                "servidor": "concorrente",
                "matricula": "20229043792",
                "thread": threading.current_thread().name,
                "custom_id": self.custom_id,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return self.error_404()
        
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python

{response_body}"""
        return response
    
    def handle_post(self, path, headers, body):
        """Processa requisições POST"""
        if path == '/submit':
            response_body = f"""
            <html>
                <body>
                    <h1>Dados Recebidos - Concorrente</h1>
                    <p>Conteúdo: {body}</p>
                    <p>Thread: {threading.current_thread().name}</p>
                    <p>Custom-ID: {self.custom_id}</p>
                    <a href="/">Voltar</a>
                </body>
            </html>
            """
            
            response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}
Server: Concorrente-Python

{response_body}"""
            return response
        else:
            return self.error_404()
    
    def error_404(self):
        """Retorna erro 404"""
        response_body = """
        <html>
            <body>
                <h1>404 - Página Não Encontrada</h1>
                <p>Recurso solicitado não existe</p>
            </body>
        </html>
        """
        
        response = f"""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.custom_id}

{response_body}"""
        return response
    
    def handle_client(self, client_socket, addr):
        """Processa um cliente em thread separada"""
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                return
            
            print(f"[{threading.current_thread().name}] Requisição de {addr}")
            
            method, path, headers, body = self.parse_http_request(data)
            
            if method == 'GET':
                response = self.handle_get(path, headers)
            elif method == 'POST':
                response = self.handle_post(path, headers, body)
            else:
                response = f"""HTTP/1.1 405 Method Not Allowed
X-Custom-ID: {self.custom_id}

<html><body><h1>405 - Método Não Permitido</h1></body></html>"""
            
            client_socket.sendall(response.encode('utf-8'))
            
        except Exception as e:
            error_response = f"""HTTP/1.1 500 Internal Server Error
X-Custom-ID: {self.custom_id}

<html><body><h1>500 - Erro Interno</h1><p>{str(e)}</p></body></html>"""
            client_socket.sendall(error_response.encode('utf-8'))
        finally:
            client_socket.close()
    
    def iniciar(self):
        """Inicia o servidor concorrente"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        
        print(f"Servidor Concorrente rodando em {self.host}:{self.port}")
        print(f"X-Custom-ID: {self.custom_id}")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Conexão aceita de {addr}")
                
                # Cria nova thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    name=f"Thread-{threading.active_count()}"
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nServidor encerrado")
        finally:
            server_socket.close()

if __name__ == "__main__":
    servidor = ServidorConcorrente()
    servidor.iniciar()