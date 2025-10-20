"""
Servidor Web Sequencial - Redes de Computadores II
Implementação usando sockets TCP puros processando uma requisição por vez
Autor: Victor Rodrigues Luz - Matrícula: 20229043792
"""

import socket
import hashlib
from datetime import datetime
import json
import time

class ServidorSequencial:
    """
    Servidor Web Sequencial implementado com sockets TCP
    Processa uma requisição por vez na porta 8080
    """
    
    def __init__(self, host='0.0.0.0', port=80):
        """
        Inicializa o servidor sequencial
        
        Args:
            host (str): Endereço IP do servidor
            port (int): Porta do servidor
        """
        self.host = host
        self.port = port
        self.customID = self.calcularCustomID()
        self.request_count = 0
        
    def calcularCustomID(self):
        """
        Calcula o X-Custom-ID baseado na matrícula e nome
        """
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"
        return hashlib.md5(dados.encode()).hexdigest()
    
    def parseHttpRequest(self, data):
        """
        Faz parsing da requisição HTTP
        """
        if not data:
            return None, None, {}, ''
            
        lines = data.split('\r\n')
        if not lines:
            return None, None, {}, ''
        
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) < 2:
            return None, None, {}, ''
        
        method = parts[0]
        path = parts[1]
        
        headers = {}
        body_start = False
        for i, line in enumerate(lines[1:], 1):
            if line == '':
                body_start = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        body = ''
        if body_start and body_start < len(lines):
            body = '\r\n'.join(lines[body_start:])
        
        return method, path, headers, body
    
    def validarCustomID(self, headers):
        """
        Valida o cabeçalho X-Custom-ID obrigatório
        """
        customID = headers.get('X-Custom-ID', '')
        return customID == self.customID
    
    def handleGet(self, path, headers):
        """
        Processa requisições GET
        """
        if not self.validarCustomID(headers):
            return self.error400("X-Custom-ID inválido ou ausente")
        
        self.request_count += 1
        current_count = self.request_count
        
        if path == '/':
            response_body = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Servidor Sequencial - Redes II</title>
                    <meta charset="utf-8">
                </head>
                <body>
                    <h1>Servidor Web Sequencial</h1>
                    <p><strong>Matrícula:</strong> 20229043792</p>
                    <p><strong>Nome:</strong> Victor Rodrigues Luz</p>
                    <p><strong>Requisição nº:</strong> {current_count}</p>
                    <p><strong>Hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>X-Custom-ID:</strong> {self.customID}</p>
                    <p><strong>Modo:</strong> Sequencial (uma requisição por vez)</p>
                    
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
            response_body = json.dumps({
                "servidor": "sequencial",
                "matricula": "20229043792",
                "nome": "Victor Rodrigues Luz",
                "customID": self.customID,
                "timestamp": datetime.now().isoformat(),
                "request_count": current_count
            }, indent=2)
            content_type = "application/json"
            
        elif path == '/stats':
            response_body = json.dumps({
                "total_requests": current_count,
                "server_type": "sequencial",
                "timestamp": datetime.now().isoformat(),
                "customID": self.customID
            }, indent=2)
            content_type = "application/json"
            
        else:
            return self.error404()
        
        response = f"""HTTP/1.1 200 OK
Content-Type: {content_type}
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{response_body}"""
        return response
    
    def handlePost(self, path, headers, body):
        """
        Processa requisições POST
        """
        if not self.validarCustomID(headers):
            return self.error400("X-Custom-ID inválido ou ausente")
        
        if path == '/submit':
            response_body = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Dados Recebidos - Sequencial</title>
                    <meta charset="utf-8">
                </head>
                <body>
                    <h1>Dados Recebidos - Servidor Sequencial</h1>
                    <p><strong>Conteúdo recebido:</strong> {body}</p>
                    <p><strong>Custom-ID:</strong> {self.customID}</p>
                    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <a href="/">Voltar para página inicial</a>
                </body>
            </html>
            """
            
            response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{response_body}"""
            return response
        else:
            return self.error404()
    
    def error400(self, message="Requisição Inválida"):
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
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II

{response_body}"""
        return response
    
    def error404(self):
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
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II

{response_body}"""
        return response
    
    def error405(self):
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
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II

{response_body}"""
        return response
    
    def processarRequisicao(self, client_socket, addr):
        start_time = time.time()
        
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return
            
            print(f"[Sequencial] Requisição de {addr}")
            
            method, path, headers, body = self.parseHttpRequest(data)
            
            print(f"[Sequencial] Método: {method}, Path: {path}")
            
            if method == 'GET':
                response = self.handleGet(path, headers)
            elif method == 'POST':
                response = self.handlePost(path, headers, body)
            else:
                response = self.error405()
            
            client_socket.sendall(response.encode('utf-8'))
            
            processing_time = time.time() - start_time
            print(f"[Sequencial] Resposta enviada em {processing_time:.4f}s")
            
        except Exception as e:
            error_response = f"""HTTP/1.1 500 Internal Server Error
Content-Type: text/html; charset=utf-8
X-Custom-ID: {self.customID}
Server: Sequencial-Python/Redes-II

<html>
<body>
    <h1>500 - Erro Interno do Servidor</h1>
    <p>{str(e)}</p>
</body>
</html>"""
            client_socket.sendall(error_response.encode('utf-8'))
            print(f"[Sequencial] Erro: {str(e)}")
            
        finally:
            client_socket.close()
            print(f"[Sequencial] Conexão com {addr} fechada")
    
    def iniciar(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print("=" * 60)
        print("SERVIDOR SEQUENCIAL - REDES DE COMPUTADORES II")
        print("=" * 60)
        print(f"Servidor rodando em: {self.host}:{self.port}")
        print(f"X-Custom-ID: {self.customID}")
        print(f"Matrícula: 20229043792")
        print(f"Nome: Victor Rodrigues Luz")
        print(f"Modo: Sequencial (uma requisição por vez)")
        print("Pressione Ctrl+C para encerrar o servidor")
        print("=" * 60)
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"\n[Sequencial] Conexão aceita de {addr}")
                self.processarRequisicao(client_socket, addr)
                print(f"[Sequencial] Próximo cliente aguardando...")
                
        except KeyboardInterrupt:
            print("\n[Sequencial] Encerrando servidor...")
        except Exception as e:
            print(f"\n[Sequencial] Erro no servidor: {str(e)}")
        finally:
            server_socket.close()
            print("[Sequencial] Socket do servidor fechado")

if __name__ == "__main__":
    servidor = ServidorSequencial()
    servidor.iniciar()