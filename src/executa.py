
from configuracoes import *
from robos import RoboAbreOS
from datetime import datetime as dt
from suporte import acrescentar_linha_em_csv, importar_linhas_de_csv


def main():
    entrada_ordens_de_servico = importar_linhas_de_csv(arquivo=ARQUIVO_ENTRADA,
                                                       extras=CAMPOS_EXTRAS)

    robo = RoboAbreOS()
    robo.criar_navegador(executavel=EXECUTAVEL,
                        url_inicial=URL_INICIAL)
    robo.logar(usuario=USUARIO, senha=SENHA)
    robo.fecha_menu_lateral()
    robo.entrada_de_ordem_de_servico()

    for ordem_de_servico in entrada_ordens_de_servico:
        try:
            numero_os = robo.abre_ordem_de_servico(os=ordem_de_servico)
            ordem_de_servico['NUMERO'] = numero_os
        except Exception:
            ordem_de_servico['NUMERO'] = 'Erro'
            robo.REGISTRO.warning('Ocorreu um erro!')
        
        # Adiciona uma data ao registro.
        ordem_de_servico['DATA'] = dt.now().strftime('%d/%m/%Y %H:%M')
        # Salva o resultado.
        acrescentar_linha_em_csv(arquivo=ARQUIVO_SAIDA,
                                linha=ordem_de_servico,
                                cabecalho=CABECALHO_SAIDA)

    robo.sair()
    robo.fechar_navegador()

if __name__ == '__main__':
    main()