import re
import os
import time


def luhn_checksum(numero):
    numeros = [int(digito) for digito in numero[::-1]]
    soma = sum(numeros[::2]) + sum(sum(divmod(digito * 2, 10)) for digito in numeros[1::2])
    return soma % 10 == 0


def buscar_padroes_dados_sensiveis(caminho_arquivo):
    padrao_cartao_credito = re.compile(r'\b(?:\d[ -]*?){13,19}\b')

    with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            correspondencias = padrao_cartao_credito.finditer(linha)
            for correspondencia in correspondencias:
                numero_cartao = correspondencia.group().replace(' ', '').replace('-', '')
                if len(numero_cartao) >= 13 and luhn_checksum(numero_cartao):
                    print(
                        f"Potencial dado sensível encontrado na linha {numero_linha} do arquivo {caminho_arquivo}: {correspondencia.group()} (Válido)")
                else:
                    print(
                        f"Potencial dado sensível encontrado na linha {numero_linha} do arquivo {caminho_arquivo}: {correspondencia.group()} (Inválido)")


def buscar_logs_em_todas_as_pastas():
    for diretorio_raiz, _, arquivos in os.walk('D:\\'):
        for arquivo in arquivos:
            if arquivo.endswith('.log'):
                caminho_arquivo = os.path.join(diretorio_raiz, arquivo)
                buscar_padroes_dados_sensiveis(caminho_arquivo)


def monitorar_mudancas():
    while True:
        # Limpar o terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        buscar_logs_em_todas_as_pastas()
        time.sleep(60)  # Verificar a cada 5 minutos (ajuste conforme necessário)


if __name__ == "__main__":
    monitorar_mudancas()
