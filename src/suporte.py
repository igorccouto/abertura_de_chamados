import os
import csv
import logging


def get_logger(name):
    """Creates a instance logger

    Return
    ------
    logger : logging.Logger
        A logger itself.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # Set a handler
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        # Set a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(process)s - %(message)s')
        handler.setFormatter(formatter)
        # Add handler to logger
        logger.addHandler(handler)
    return logger

def acrescentar_linha_em_csv(arquivo, linha, cabecalho, delimitador=';', quotecarac='"'):
    """Acrescenta uma linha ao arquivo CSV.
    
    Parâmetros
    ----------
    arquivo : str
        Caminho do arquivo CSV.
    linha : dict
        Dicionário contendo as informações a serem acrescentadas no arquivo.
    cabecalho:
        Quais campos serão adicionados ao arquivo.
    """
    # Verifica se arquivo já existe.
    existe=False
    if os.path.exists(arquivo):
        existe=True

    try:
        with open(arquivo, 'a', newline='') as f:
            writer = csv.DictWriter(f, delimiter=delimitador, quotechar=quotecarac, fieldnames=cabecalho)

            if not existe:
                writer.writeheader()

            linha_filtrada = {k: v for k, v in linha.items() if k in cabecalho}
            writer.writerow(linha_filtrada)
    except PermissionError:
        print('PermissionError: Não foi possível acrescentar linha em %s. Arquivo indisponível.' % arquivo)

def importar_linhas_de_csv(arquivo, extras={}, delimitador=';', quotecarac='"'):
    """Importa linhas de arquivo CSV.
    
    Parâmetros
    ----------
    arquivo : str
        Caminho do arquivo CSV.
    
    Retorno
    -------
    linhas : list
        Lista de dicionários contendo as linhas do arquivo. Cada dicionário é uma linha do arquivo.
    """
    linhas = []
    with open(arquivo, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimitador, quotechar=quotecarac)

        for r in reader:
            linha = dict(r)
            # Acrescenta os campos de extras.
            linha = {**linha, **extras}
            # Adiciona à lista final.
            linhas.append(linha)
    return linhas