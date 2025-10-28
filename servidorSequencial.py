import socket
import hashlib
from datetime import datetime
import time
import json

class ServidorSequencial:
    def __init__(self, host='37.92.0.10', porta=80):
        self.host = host # IP do servidor
        self.porta = porta # Porta de escuta
        self.id_personalizado = self.calcular_id_personalizado() # Gera um ID único
        self.contador_requisicoes = 0
        
    def calcular_id_personalizado(self):
        matricula = "20229043792"
        nome = "Victor Rodrigues Luz"
        dados = f"{matricula} {nome}"

        return hashlib.md5(dados.encode()).hexdigest() # Retorna o hash MD5
    
    def analisar_requisicao_http(self, dados):
        """Faz análise manual da requisição HTTP -> Não foi usada nenhuma biblioteca HTTP (tipo Flask ou FastAPI). 
           Por conta disso,  o servidor precisa entender sozinho o que o cliente mandou: método (GET, POST...), caminho, cabeçalhos e etc"""
        try:
            linhas = dados.split('\r\n')
            if len(linhas) == 0:
                return None, None, {}, ''

            primeira_linha = linhas[0].split()
            if len(primeira_linha) < 3:
                return None, None, {}, ''

            metodo = primeira_linha[0]
            caminho = primeira_linha[1]
            
            cabecalhos = {}
            corpo = ''
            achou_vazio = False

            for i in range(1, len(linhas)):
                linha_atual = linhas[i]
                
                if linha_atual == '':
                    achou_vazio = True
                    continue
                    
                if achou_vazio:
                    corpo += linha_atual
                else:
                    if ':' in linha_atual:
                        partes = linha_atual.split(':', 1)
                        chave = partes[0].strip()
                        valor = partes[1].strip()
                        cabecalhos[chave] = valor

            return metodo, caminho, cabecalhos, corpo.strip()
            
        except:
            return None, None, {}, ''
    
    def validar_id_personalizado(self, cabecalhos):
        """Verifica se o cliente que fez a requisição HTTP enviou o X-Custom-ID com o valor correto (igual o gerado pelo servidor)"""
        return cabecalhos.get('X-Custom-ID') == self.id_personalizado
    
    def criar_resposta_http(self, codigo_status, conteudo, tipo_conteudo="text/html", cabecalhos_personalizados=None):
        """Cria resposta HTTP manualmente (status, cabeçalhos e corpo)"""
        mensagens_status = {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }

        # "/r" -> retorno do cursor para o início da linha. Juntos,"\r\n" representam uma quebra de linha padrão no protocolo HTTP, que é baseado no padrão do protocolo TCP.
        resposta = f"HTTP/1.1 {codigo_status} {mensagens_status.get(codigo_status, 'Unknown')}\r\n" # resposta HTTP (enviada pelo servidor)
        
        # Em cima eu criei o "status", já aqui em baixo será montado o cabeçalho
        resposta += f"Content-Type: {tipo_conteudo}; charset=utf-8\r\n" # Diz ao conteiner o tipo de conteúdo (HTML, JSON, etc.)
        resposta += f"X-Custom-ID: {self.id_personalizado}\r\n" # Cabeçalho personalizado X-Custom-ID, que servidor exige para validar a requisição
        resposta += f"Server: Sequencial-Socket/Redes-II\r\n" # Identifica o servidor que está respondendo.
        resposta += f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n" # Data e hora da resposta, no formato padrão HTTP
        resposta += f"Content-Length: {len(conteudo.encode('utf-8'))}\r\n" # tamanho do corpo da resposta em bytes. Serve para cliente saber quando a resposta termina.
        resposta += "Connection: close\r\n" # Diz que a conexão será encerrada após essa "resposta"
        
        if cabecalhos_personalizados: # Opicional
            for chave, valor in cabecalhos_personalizados.items():
                resposta += f"{chave}: {valor}\r\n"
        
        resposta += "\r\n"
        resposta += conteudo
        
        return resposta
    
    def processar_requisicao_get(self, caminho, cabecalhos):
        """Processa requisições GET"""
        if not self.validar_id_personalizado(cabecalhos):
            return self.criar_resposta_http(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>") # senha está errada
        
        self.contador_requisicoes += 1 # contador

        # Ver o que foi PEDIDO e ENTREGUE:
        if caminho == '/' or caminho == '/index.html':
            conteudo = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Servidor Sequencial - Sockets</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Servidor Web Sequencial com Sockets Brutos</h1>
    <p><strong>Matrícula:</strong> 20229043792</p>
    <p><strong>Nome:</strong> Victor Rodrigues Luz</p>
    <p><strong>Requisição nº:</strong> {self.contador_requisicoes}</p>
    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>X-Custom-ID:</strong> {self.id_personalizado}</p>
    <p><strong>Tipo:</strong> Sequencial (Socket TCP Bruto)</p>
</body>
</html>
"""
            return self.criar_resposta_http(200, conteudo, "text/html")
            
        elif caminho == '/info':
            info = {
                "servidor": "sequencial_socket",
                "matricula": "20229043792",
                "nome": "Victor Rodrigues Luz",
                "custom_id": self.id_personalizado,
                "timestamp": datetime.now().isoformat(),
                "request_count": self.contador_requisicoes,
                "protocol": "TCP/Socket"
            }
            return self.criar_resposta_http(200, json.dumps(info, indent=2), "application/json")
            
        elif caminho == '/status':
            status_info = {
                "status": "online",
                "server_type": "sequential",
                "requests_processed": self.contador_requisicoes,
                "uptime": "since_start",
                "custom_id_valid": True
            }
            return self.criar_resposta_http(200, json.dumps(status_info, indent=2), "application/json")
            
        else:
            return self.criar_resposta_http(404, "<h1>404 - Recurso Não Encontrado</h1><p>Use: /, /info, /status</p>")
    
    def processar_requisicao_post(self, caminho, cabecalhos, corpo):
        """Processa requisições POST"""
        if not self.validar_id_personalizado(cabecalhos):
            return self.criar_resposta_http(400, "<h1>400 - X-Custom-ID inválido ou ausente</h1>") # senha está errada
        
        self.contador_requisicoes += 1 # contador
        
        # Ver o que foi PEDIDO e ENTREGUE:
        if caminho == '/api/data':
            time.sleep(0.01)
            
            dados_resposta = {
                "status": "received",
                "data_length": len(corpo),
                "processed_at": datetime.now().isoformat(),
                "request_id": self.contador_requisicoes,
                "custom_id": self.id_personalizado
            }
            return self.criar_resposta_http(200, json.dumps(dados_resposta, indent=2), "application/json")
            
        elif caminho == '/api/echo':
            resposta_echo = {
                "echo": corpo,
                "timestamp": datetime.now().isoformat(),
                "received_bytes": len(corpo)
            }
            return self.criar_resposta_http(200, json.dumps(resposta_echo, indent=2), "application/json")
            
        else:
            return self.criar_resposta_http(404, "<h1>404 - Endpoint POST não encontrado</h1>")
    
    def processar_requisicao(self, socket_cliente, endereco_cliente):
        """Processa uma requisição individual"""
        try:
            dados_requisicao = b""
            socket_cliente.settimeout(5.0)
            
            while True:
                pedaco = socket_cliente.recv(1024) # Pega pedaços de 1KB
                if not pedaco:
                    break
                dados_requisicao += pedaco # Aqui ele junta todos os pedaços
                if b'\r\n\r\n' in dados_requisicao:# Para quando achar linha vazia
                    break
            
            if not dados_requisicao:
                return
            
            texto_requisicao = dados_requisicao.decode('utf-8', errors='ignore') # Converte bytes para texto
            metodo, caminho, cabecalhos, corpo = self.analisar_requisicao_http(texto_requisicao) # a função analizar_requisicao_http organiza a mesnagem de forma manual
            
            print(f"[Sequencial] {endereco_cliente} - {metodo} {caminho}")
            
            if metodo == 'GET':
                resposta = self.processar_requisicao_get(caminho, cabecalhos)
            elif metodo == 'POST':
                resposta = self.processar_requisicao_post(caminho, cabecalhos, corpo)
            elif metodo == 'HEAD':
                if caminho == '/':
                    conteudo = ""
                    resposta = self.criar_resposta_http(200, conteudo, "text/html")
                else:
                    resposta = self.criar_resposta_http(404, "")
            else:
                resposta = self.criar_resposta_http(405, "<h1>405 - Método Não Permitido</h1>")
            
            socket_cliente.send(resposta.encode('utf-8')) # Manda uma resposta de volta
            
        except socket.timeout:
            resposta_erro = self.criar_resposta_http(408, "<h1>408 - Timeout</h1>")
            socket_cliente.send(resposta_erro.encode('utf-8'))
        except Exception as e:
            resposta_erro = self.criar_resposta_http(500, f"<h1>500 - Erro Interno</h1><p>{str(e)}</p>")
            socket_cliente.send(resposta_erro.encode('utf-8'))
        finally:
            socket_cliente.close() # fim
    
    def iniciar(self):
        """Inicia o servidor sequencial"""
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_servidor.bind((self.host, self.porta))
        socket_servidor.listen(5)
        
        print("=" * 70)
        print("SERVIDOR SEQUENCIAL - SOCKETS BRUTOS")
        print("=" * 70)
        print(f"Servidor: {self.host}:{self.porta}")
        print(f"X-Custom-ID: {self.id_personalizado}")
        print(f"Matrícula: 20229043792")
        print(f"Nome: Victor Rodrigues Luz")
        print("Endpoints: GET /, /info, /status")
        print("Endpoints: POST /api/data, /api/echo")
        print("Pressione Ctrl + C para encerrar")
        print("=" * 70)
        
        try:
            while True:
                socket_cliente, endereco_cliente = socket_servidor.accept()
                print(f"\n[Sequencial] Conexão aceita: {endereco_cliente}")
                
                self.processar_requisicao(socket_cliente, endereco_cliente)
                
                print(f"[Sequencial] Requisição concluída: {endereco_cliente}")
                
        except KeyboardInterrupt:
            print("\n[Sequencial] Encerrando servidor...")
        except Exception as e:
            print(f"\n[Sequencial] Erro: {e}")
        finally:
            socket_servidor.close()

if __name__ == "__main__":
    servidor = ServidorSequencial()
    servidor.iniciar()