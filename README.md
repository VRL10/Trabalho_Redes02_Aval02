# Projeto Redes II - Comparação Servidores Web

## Sobre o Projeto
Comparação de desempenho entre servidores web Sequencial vs Concorrente implementados com sockets TCP brutos em Python.

## Para obter o software temos 2 opções:

### Opção 1: Clone do Repositório
```
git clone https://github.com/VRL10/Trabalho_Redes02_Aval02.git
cd Trabalho_Redes02_Aval02
```

### Opção 2: Download ZIP
- Acesse: https://github.com/VRL10/Trabalho_Redes02_Aval02
- Clique em "Code" → "Download ZIP"
- Extraia e entre na pasta

## Pré-requisitos:
- Docker
- Docker Compose

## Passo a passo de como executar o programa:

### 1°. Limpar ambiente (opcional - se já executou antes)
```
docker-compose down
docker system prune -f
```

### 2°. Executar os testes
```
docker-compose up
```

## IMPORTANTE: Leia isso antes de executar

### COMO FUNCIONA:
- Testes 100% automáticos - você não precisa fazer nada!
- Tempo estimado: Até 10 minutos para conclusão total.
- Processo automático:
  - Sobe servidores sequencial e concorrente
  - Executa 1.200 requisições distribuídas em 3 cenários
  - Salva resultados automaticamente
  - SERVIDORES CONTINUAM RODANDO (comportamento normal). Pode parecer que o software travou, mas na verdade os servidores apenas continuaram esperando mais conexões.

- Quando os testes terminarem você verá que aparecerá um arquivo chamado "metricas_completas" dentro da pasta resultados.

## Resultados
Os resultados ficam salvos na sua máquina em: ./resultados/metricas_completas.json

## No fim de tudo teremos:
- Build das imagens Docker
- Criação da rede 37.92.0.0/16
- Servidores sobem e ficam ativos esperando conexões
- Cliente executa automaticamente:
  - 3 cenários de carga (baixa, média, alta)
  - 10 execuções por cenário
  - 1.200 requisições totais
- Salva resultados em resultados/
- Servidores continuam rodando (comportamento esperado)

Link do Vídeo do Youtube:
Vídeo Principal: https://youtu.be/cjEnH0GhgP8
Vídeo de Comprovação (Executando os testes passo a passo até chegar nos resultados): https://youtu.be/cjEnH0GhgP8
