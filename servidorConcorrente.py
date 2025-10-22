import socket
import hashlib
from datetime import datetime
import time
import threading
import json

class ServidorConcorrente:
    def __init__(self, host='37.92.0.11', porta=80):
        self.host = host
        self.porta = porta
        self.idCustom = self.calcularIdCustom()
        self.request_counter = 0
        self.counter_lock = threading.Lock()
        
    def calcularIdCustom(self):
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def parse_http_request(self, data):
        """Faz parsing manual da requisição HTTP"""
        try:
            lines = data.split('\r\n')
            if not lines:
                return None, None, {}, ''
            
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) < 3:
                return None, None, {}, ''
                
            method = parts[0]
            path = parts[1]
            version = parts[2]
            
            headers = {}
            body = ''
            empty_line_found = False
            
            for line in lines[1:]:
                if not line:
                    empty_line_found = True
                    continue
                    
                if not empty_line_found and ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
                elif empty_line_found:
                    body += line
            
            return method, path, headers, body.strip()
            
        except Exception as e:
            return None, None, {}, ''
    
    def validate_custom_id(self, headers):
        """Valida o X-Custom-ID obrigatório"""
        return headers.get('X-Custom-ID') == self.idCustom
    
    def create_http_response(self, status_code, content, content_type="text/html", custom_headers=None):
        """Cria resposta HTTP manualmente"""
        status_messages = {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        
        response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
        response += f"Content-Type: {content_type}; charset=utf-8\r\n"
        response += f"X-Custom-ID: {self.idCustom}\r\n"
        response += f"Server: Concorrente-Socket/Redes-II\r\n"
        response += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response += f"Content-Length: {len(content.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        
        if custom_headers:
            for key, value in custom_headers.items():
                response += f"{key}: {value}\r\n"
        
        response += "\r\n"
        response += content
        
        return response
    
    def handle_get_request(self, path, headers):
        """Processa requisições GET"""
        if not self.validate_custom_id(headers):
            return self.create_http_response(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>")
        
        with self.counter_lock:
            self.request_counter += 1
            current_count = self.request_counter
        
        if path == '/' or path == '/index.html':
            content = f"""
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
    <p><strong>Requisição nº:</strong> {current_count}</p>
    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>X-Custom-ID:</strong> {self.idCustom}</p>
    <p><strong>Tipo:</strong> Concorrente (Socket TCP + Threads)</p>
</body>
</html>
"""
            return self.create_http_response(200, content, "text/html")
            
        elif path == '/info':
            info = {
                "servidor": "concorrente_socket",
                "matricula": "20229043792",
                "nome": "Victor Rodrigues Luz",
                "thread": threading.current_thread().name,
                "custom_id": self.idCustom,
                "timestamp": datetime.now().isoformat(),
                "request_count": current_count,
                "protocol": "TCP/Socket",
                "concurrency": "thread-based"
            }
            return self.create_http_response(200, json.dumps(info, indent=2), "application/json")
            
        elif path == '/status':
            status_info = {
                "status": "online",
                "server_type": "concurrent",
                "requests_processed": current_count,
                "active_threads": threading.active_count(),
                "thread_name": threading.current_thread().name,
                "custom_id_valid": True
            }
            return self.create_http_response(200, json.dumps(status_info, indent=2), "application/json")
            
        elif path == '/heavy':
            time.sleep(2)
            content = {
                "operation": "heavy_processing",
                "duration": "2 seconds",
                "thread": threading.current_thread().name,
                "timestamp": datetime.now().isoformat()
            }
            return self.create_http_response(200, json.dumps(content, indent=2), "application/json")
            
        else:
            return self.create_http_response(404, "<h1>404 - Recurso Não Encontrado</h1><p>Use: /, /info, /status, /heavy</p>")
    
    def handle_post_request(self, path, headers, body):
        """Processa requisições POST"""
        if not self.validate_custom_id(headers):
            return self.create_http_response(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>")
        
        with self.counter_lock:
            self.request_counter += 1
            current_count = self.request_counter
        
        if path == '/api/data':
            processing_time = 0.1
            time.sleep(processing_time)
            
            response_data = {
                "status": "processed",
                "data_received": body,
                "data_length": len(body),
                "processing_time": f"{processing_time}s",
                "processed_at": datetime.now().isoformat(),
                "request_id": current_count,
                "thread": threading.current_thread().name,
                "custom_id": self.idCustom
            }
            return self.create_http_response(200, json.dumps(response_data, indent=2), "application/json")
            
        elif path == '/api/echo':
            echo_response = {
                "echo": body,
                "timestamp": datetime.now().isoformat(),
                "received_bytes": len(body),
                "thread": threading.current_thread().name
            }
            return self.create_http_response(200, json.dumps(echo_response, indent=2), "application/json")
            
        elif path == '/api/batch':
            time.sleep(0.5)
            batch_response = {
                "operation": "batch_processing",
                "items_processed": len(body.split(',')),
                "processing_time": "0.5s",
                "thread": threading.current_thread().name,
                "timestamp": datetime.now().isoformat()
            }
            return self.create_http_response(200, json.dumps(batch_response, indent=2), "application/json")
            
        else:
            return self.create_http_response(404, "<h1>404 - Endpoint POST não encontrado</h1>")
    
    def handle_client(self, client_socket, client_address):
        """Processa um cliente em thread separada"""
        thread_name = threading.current_thread().name
        start_time = time.time()
        
        try:
            request_data = b""
            client_socket.settimeout(10.0)
            
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                request_data += chunk
                if b'\r\n\r\n' in request_data:
                    break
            
            if not request_data:
                return
            
            request_text = request_data.decode('utf-8', errors='ignore')
            method, path, headers, body = self.parse_http_request(request_text)
            
            print(f"[{thread_name}] {client_address} - {method} {path}")
            
            if method == 'GET':
                response = self.handle_get_request(path, headers)
            elif method == 'POST':
                response = self.handle_post_request(path, headers, body)
            elif method == 'HEAD':
                if path == '/':
                    response = self.create_http_response(200, "", "text/html")
                else:
                    response = self.create_http_response(404, "")
            else:
                response = self.create_http_response(405, "<h1>405 - Método Não Permitido</h1>")
            
            client_socket.send(response.encode('utf-8'))
            
            processing_time = time.time() - start_time
            print(f"[{thread_name}] Resposta enviada em {processing_time:.3f}s")
            
        except socket.timeout:
            error_response = self.create_http_response(408, "<h1>408 - Timeout</h1>")
            client_socket.send(error_response.encode('utf-8'))
            print(f"[{thread_name}] Timeout com {client_address}")
        except Exception as e:
            error_response = self.create_http_response(500, f"<h1>500 - Erro Interno</h1><p>{str(e)}</p>")
            client_socket.send(error_response.encode('utf-8'))
            print(f"[{thread_name}] Erro: {e}")
        finally:
            client_socket.close()
            print(f"[{thread_name}] Conexão fechada: {client_address}")
    
    def start(self):
        """Inicia o servidor concorrente"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.porta))
        server_socket.listen(10)
        
        print("=" * 70)
        print("SERVIDOR CONCORRENTE - SOCKETS BRUTOS")
        print("=" * 70)
        print(f"Servidor: {self.host}:{self.porta}")
        print(f"X-Custom-ID: {self.idCustom}")
        print(f"Matrícula: 20229043792")
        print(f"Nome: Victor Rodrigues Luz")
        print("Endpoints: GET /, /info, /status, /heavy")
        print("Endpoints: POST /api/data, /api/echo, /api/batch")
        print("Pressione Ctrl+C para encerrar")
        print("=" * 70)
        
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"\n[Main] Conexão aceita: {client_address}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    name=f"Thread-{threading.active_count()}"
                )
                client_thread.daemon = True
                client_thread.start()
                
                print(f"[Main] Thread iniciada: {client_thread.name}")
                print(f"[Main] Threads ativas: {threading.active_count() - 1}")
                
        except KeyboardInterrupt:
            print("\n[Main] Encerrando servidor...")
        except Exception as e:
            print(f"\n[Main] Erro: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    servidor = ServidorConcorrente()
    servidor.start()