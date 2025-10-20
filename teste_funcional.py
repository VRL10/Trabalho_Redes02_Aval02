"""
Teste Funcional dos Servidores - Redes de Computadores II
Testa se GET e POST estão funcionando corretamente
"""

import socket
import hashlib

def calcularCustomID():
    matricula = "20229043792"
    nome = "Victor Rodrigues Luz"
    dados = f"{matricula} {nome}"
    return hashlib.md5(dados.encode()).hexdigest()

def testarGET(host, porta, nomeServidor):
    print(f"Testando GET em {nomeServidor} ({host}:{porta})")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, porta))
        
        customID = calcularCustomID()
        requisicao = f"""GET / HTTP/1.1
Host: {host}:{porta}
X-Custom-ID: {customID}
User-Agent: Teste-Funcional
Connection: close

"""
        requisicao = requisicao.replace('\n', '\r\n')
        
        sock.sendall(requisicao.encode())
        resposta = sock.recv(4096).decode()
        
        print("STATUS: Conexão estabelecida com sucesso")
        
        if "200 OK" in resposta:
            print("STATUS: GET / - OK (200)")
        else:
            print("STATUS: GET / - FALHA")
            
        if "Victor Rodrigues Luz" in resposta:
            print("STATUS: Nome do aluno - OK")
        else:
            print("STATUS: Nome do aluno - FALHA")
            
        if "20229043792" in resposta:
            print("STATUS: Matrícula - OK")
        else:
            print("STATUS: Matrícula - FALHA")
            
        print(f"Resposta (início): {resposta[:200]}...")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def testarPOST(host, porta, nomeServidor):
    print(f"Testando POST em {nomeServidor} ({host}:{porta})")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, porta))
        
        customID = calcularCustomID()
        dados = "dados=teste_funcional"
        requisicao = f"""POST /submit HTTP/1.1
Host: {host}:{porta}
X-Custom-ID: {customID}
User-Agent: Teste-Funcional
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(dados)}
Connection: close

{dados}"""
        requisicao = requisicao.replace('\n', '\r\n')
        
        sock.sendall(requisicao.encode())
        resposta = sock.recv(4096).decode()
        
        print("STATUS: Conexão estabelecida com sucesso")
        
        if "200 OK" in resposta:
            print("STATUS: POST /submit - OK (200)")
        else:
            print("STATUS: POST /submit - FALHA")
            
        if "teste_funcional" in resposta:
            print("STATUS: Dados recebidos - OK")
        else:
            print("STATUS: Dados recebidos - FALHA")
            
        print(f"Resposta (início): {resposta[:200]}...")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def testarEndpointInfo(host, porta, nomeServidor):
    print(f"Testando /info em {nomeServidor} ({host}:{porta})")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, porta))
        
        customID = calcularCustomID()
        requisicao = f"""GET /info HTTP/1.1
Host: {host}:{porta}
X-Custom-ID: {customID}
User-Agent: Teste-Funcional
Connection: close

"""
        requisicao = requisicao.replace('\n', '\r\n')
        
        sock.sendall(requisicao.encode())
        resposta = sock.recv(4096).decode()
        
        print("STATUS: Conexão estabelecida com sucesso")
        
        if "200 OK" in resposta:
            print("STATUS: GET /info - OK (200)")
        else:
            print("STATUS: GET /info - FALHA")
            
        if "application/json" in resposta:
            print("STATUS: Content-Type JSON - OK")
        else:
            print("STATUS: Content-Type JSON - FALHA")
            
        print(f"Resposta (início): {resposta[:200]}...")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def executarTestesCompletos():
    print("INICIANDO TESTES FUNCIONAIS")
    print("=" * 60)
    
    # Testar Servidor Sequencial
    print("\n--- SERVIDOR SEQUENCIAL (localhost:8080) ---")
    testarGET("localhost", 8080, "Sequencial")
    testarPOST("localhost", 8080, "Sequencial") 
    testarEndpointInfo("localhost", 8080, "Sequencial")
    
    # Testar Servidor Concorrente
    print("\n--- SERVIDOR CONCORRENTE (localhost:8081) ---")
    testarGET("localhost", 8081, "Concorrente")
    testarPOST("localhost", 8081, "Concorrente")
    testarEndpointInfo("localhost", 8081, "Concorrente")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")

if __name__ == "__main__":
    executarTestesCompletos()