from decouple import config


ARQUIVO_ENTRADA = 'ordens_de_servico.csv'
ARQUIVO_SAIDA = 'ordens_de_servico_abertas.csv'

CABECALHO_SAIDA = ['DATA', 'NUMERO', 'PIB', 'PRIORIDADE', 'PROBLEMA', 'DESCRICAO']

EXECUTAVEL = 'chromedriver/chromedriver.exe'
URL_INICIAL = 'http://erp'

USUARIO = config('USUARIO')
SENHA = config('SENHA')
EMAIL = config('EMAIL')
CODIGO_ANS_FISCAL = config('CODIGO_ANS_FISCAL')

CAMPOS_EXTRAS = {'CADASTRO_FISCAL': CODIGO_ANS_FISCAL,
                 'MATRICULA_FISCAL': USUARIO,
                 'EMAIL': EMAIL}