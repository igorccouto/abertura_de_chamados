from time import sleep
from suporte import get_logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class RoboAbreOS():
    def criar_navegador(self, executavel, url_inicial, tempo_de_espera=60):
        """Cria um navegador Chrome para acessar o sistema.
        Parâmetros
        ----------
        url_inicial : str
            O endereço URL do sistema.
        tempo_de_espera : int
            Tempo de espera em segundos pelas respostas do sistema. Padrão de 60 segundos.
        ----------
        """
        opt = webdriver.ChromeOptions()
        #opt.add_argument('--headless')
        opt.add_argument('--start-maximized')
        self.DRIVER = webdriver.Chrome(executable_path=executavel,
                                       options=opt)
        self.DRIVER.get(url_inicial)
        self.WAIT = WebDriverWait(self.DRIVER, tempo_de_espera)
        self.ACTION = ActionChains(self.DRIVER)
        self.REGISTRO = get_logger('RoboAbreOS')

    def logar(self, usuario, senha):
        """Loga no sistema usando usuário e senha informados.

        Parãmetros
        ----------
        usuario : str
            Usuário com acesso ao sistema.
        senha : str
            Senha do usuário.
        """
        self.WAIT.until(lambda d: d.find_element_by_id('User')).send_keys(usuario)
        self.WAIT.until(lambda d: d.find_element_by_id('Password')).send_keys(senha)
        self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@value="Login"]')).click()
        self.NOME_FISCAL = self.WAIT.until(lambda d: d.find_element_by_id('usernameDiv')).text
        self.REGISTRO.info('Acessando com o colaborador %s.' % self.NOME_FISCAL)

    def fecha_menu_lateral(self):
        """Fecha o menu lateral para melhor visualização.
        """
        try:
            carrossel = self.WAIT.until(lambda d: d.find_element_by_id('caroBar')).get_attribute('title')
            if carrossel == 'Ocultar Carrossel':
                self.WAIT.until(lambda d: d.find_element_by_id('caroBar')).click()
        except TimeoutException:
            pass

    def entrada_de_ordem_de_servico(self):
        """Abre o módulo para entrada de ordens de serviço.
        """
        self.DRIVER.switch_to.default_content()
        # Aguarda menu carregar
        self.WAIT.until(lambda d: d.find_element_by_id('menuContainer'))
        self.WAIT.until(lambda d: d.find_element_by_id('drop_mainmenu')).click()
        self.WAIT.until(ec.visibility_of_element_located((By.XPATH,
                                                          '//*[@tasklabel="Correios"]'))).click()
        self.WAIT.until(ec.visibility_of_element_located((By.XPATH,
                                                          '//*[@tasklabel="Manutenção"]'))).click()
        self.WAIT.until(ec.visibility_of_element_located((By.XPATH, 
                                                          '//*[@tasklabel="Ordem de Serviço"]'))).click()
        self.WAIT.until(ec.visibility_of_element_located((By.XPATH, 
                                                          '//*[@tasklabel="Entrada de Ordem de Serviço"]'))).click()
        self.WAIT.until(lambda d: d.find_element_by_xpath(
            '//div[@id="e1BreadcrumbBar"]//div[contains(text(), "Ordem de Serviço")]'
        ))
        self.REGISTRO.info('Acessando "Entrada de Ordem de Serviço".')

    def abre_ordem_de_servico(self, os):
        """ No módulo de Entrada de Ordem de Serviço, executa o processo de inclusão de uma nova ordem de serviço.
        
        Parâmetros
        ----------
        os : dict
            Um dicionário contendo informações da ordem de serviço.

        Retorno
        -------
        numero_os : str
            Número da ordem de serviço aberta.
        """
        self.REGISTRO.info('Abrindo OS para %s.' % os['PIB'])

        self.DRIVER.switch_to.default_content()
        # Trata as informações de entrada.
        os['PROBLEMA'] = os['PROBLEMA'][:30]
        os['DESCRICAO'] = os['DESCRICAO'][:80]
        DESCRICAO = '%s. Email: %s. Telefone: (%s) %s. Endereço: %s. %s. %s' % (os['DESCRICAO_LONGA'],
                                                                                os['EMAIL'],
                                                                                os['DDD'],
                                                                                os['TELEFONE'],
                                                                                os['LOGRADOURO'],
                                                                                os['CEP'],
                                                                                os['BAIRRO'])
        # Mudanca de contexto
        e1menuAppIframe = self.WAIT.until(
            ec.visibility_of_element_located((By.ID, 'e1menuAppIframe'))
        )
        self.DRIVER.switch_to.frame(e1menuAppIframe)

        # Clica em Incluir
        self.WAIT.until(lambda d: d.find_element_by_id('hc_Add')).click()

        # Insere *<PIB>
        pib = self.WAIT.until(
            lambda d: d.find_element_by_xpath('//input[@title="Asset Number_ASII"]'
        ))
        pib.send_keys('*%s' % os['PIB'])
        self.ACTION.send_keys(Keys.TAB).perform()

        # Espera aparecer o tipo de aparelho
        tipo_equipamento = self.WAIT.until(lambda d: d.find_element_by_xpath(
            '//input[@title="Asset Number_ASII"]/following::div[1]/span[@class="FieldLabel"]/i[text()]'
        )).text
        self.REGISTRO.info('   Equipamento %s' % tipo_equipamento)

        # Descrição
        descricao = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Descrição"]'))
        sleep(1)
        descricao.send_keys(os['DESCRICAO'])

        # Problema
        problema = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Problema"]'))
        sleep(1)
        problema.send_keys(os['PROBLEMA'])

        # Prioridade
        prioridade = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Prioridade"]'))
        sleep(1)
        prioridade.send_keys(os['PRIORIDADE'])

        # Insere "Peg para OS"
        peg_para_os = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Peg para OS"]'))
        sleep(1)
        peg_para_os.send_keys(os['CADASTRO_FISCAL'])

        # Insere "Nº do Cadastro"
        self.WAIT.until(
            lambda d: d.find_element_by_xpath('//input[@title="Customer Number _ ALKY"]'
        )).send_keys(os['CADASTRO_FISCAL'])

        # Insere "Designado a"
        designado_a = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Assigned To Address Number_ ALKY"]'))
        sleep(1)
        designado_a.send_keys(os['FORNECEDOR'])
        self.ACTION.send_keys(Keys.TAB).perform()
        fornecedor = self.WAIT.until(lambda d: d.find_element_by_xpath(
            '//input[@title="Assigned To Address Number_ ALKY"]/following::div[1]/span[@class="FieldLabel"]/i[text()]'
        )).text
        self.REGISTRO.info('   Designado a %s' % fornecedor)

        # Insere "Originador"
        originador = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Originator Address Number_ ALKY"]'))
        sleep(1)
        originador.send_keys(os['CADASTRO_FISCAL'])
        self.ACTION.send_keys(Keys.TAB).perform()
        originador = self.WAIT.until(lambda d: d.find_element_by_xpath(
            '//input[@title="Originator Address Number_ ALKY"]/following::div[1]/span[@class="FieldLabel"]/i[text()]'
        )).text
        self.REGISTRO.info('   Originador %s' % originador)

        # Insere "Matr. Cliente"
        matr_cliente = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Matr. Cliente"]'))
        sleep(1)
        matr_cliente.send_keys(os['MATRICULA_FISCAL'])
        # Aguarda janela com codigos aparecer e clica nela.
        self.WAIT.until(
            ec.visibility_of_element_located((By.ID, 'typeAheadWindow'))
        ).click()
        self.WAIT.until(lambda d: d.find_element_by_xpath('//*[@title="Matr. Cliente"]/following::span/i[text()="%s"]' % self.NOME_FISCAL))

        # Insere "DDD"
        ddd = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="DDD"]'))
        ddd.clear()
        sleep(1)
        ddd.send_keys(os['DDD'])

        # Insere "Telefone"
        telefone = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Telefone"]'))
        telefone.clear()
        sleep(1)
        telefone.send_keys(os['TELEFONE'])

        # Insere "CEP"
        cep = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="CEP"]'))
        cep.clear()
        sleep(1)
        cep.send_keys(os['CEP'])

        # Insere "Logradouro Equip."
        logradouro = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Logradouro Equip."]'))
        logradouro.clear()
        sleep(1)
        logradouro.send_keys(os['LOGRADOURO'])

        # Insere "Bairro"
        bairro = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Bairro"]'))
        bairro.clear()
        sleep(1)
        bairro.send_keys(os['BAIRRO'])

        # Insere "Municipio"
        municipio = self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Município"]'))
        municipio.clear()
        sleep(1)
        municipio.send_keys(os['CODIGO_MUNICIPIO'])

        # Aguarda janela com codigos aparecer.
        self.WAIT.until(
            ec.visibility_of_element_located((By.ID, 'typeAheadWindow'))
        )

        # Abre a aba "Descrição Longa da O.S."
        self.WAIT.until(lambda d: d.find_element_by_link_text('Descrição Longa da O.S.')).click()

        # Insere "Descricao_Longa_OS"
        self.WAIT.until(lambda d: d.find_element_by_xpath('//textarea[@title="Descricao_Longa_OS"]')).send_keys(DESCRICAO)

        # "Salvar e Sair"
        self.WAIT.until(lambda d: d.find_element_by_xpath('//button[text()="Salvar e Sair"]')).click()

        # Aguarda alerta.
        self.WAIT.until(lambda d: d.find_element_by_link_text('Garantia em Prática'))

        # Clica em "Salvar e Sair" novamente
        self.WAIT.until(lambda d: d.find_element_by_xpath('//button[text()="Salvar e Sair"]')).click()

        # Aguarda formulário de confirmação
        self.WAIT.until(lambda d: d.find_element_by_xpath('//*[@id="jdeFormTitle0" and contains(text(),"Status")]'))
        
        # Confirma
        painel_confirmacao = self.WAIT.until(lambda d: d.find_element_by_id('E1PaneForm'))
        painel_confirmacao.find_element_by_xpath('//img[@title="OK (Ctrl+Alt+O)"]').click()

        # Procura OS pela PIB
        self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Número Unidade"]')).clear()
        self.WAIT.until(lambda d: d.find_element_by_xpath('//input[@title="Número Unidade"]')).send_keys(os['PIB'])

        # Clica em Procurar
        self.WAIT.until(lambda d: d.find_element_by_xpath('//img[@title="Procurar (Ctrl+Alt+I)"]')).click()

        numero_os = self.WAIT.until(lambda d: d.find_element_by_xpath('//*[@id="jdeGridData0_1.0"]//a[text()]')).text

        self.REGISTRO.info('   Número OS ERP: %s' % numero_os)

        return numero_os

    def sair(self):
        """Sai do sistema.
        """
        try:
            self.DRIVER.switch_to.default_content()
            self.WAIT.until(lambda d: d.find_element_by_id('userAndEnvContainer')).click()
            self.WAIT.until(lambda d: d.find_element_by_id('signOutLinkDiv')).click()
            self.DRIVER.switch_to.alert.accept()
            self.REGISTRO.info('Saindo do sistema.')
        except TimeoutException:
            self.REGISTRO.info('Não foi possível sair do sistema.')
            pass
        except NoAlertPresentException:
            pass

    def fechar_navegador(self):
        """Fecha navegador.
        """
        self.REGISTRO.info('Fechando navehador.')
        self.DRIVER.quit()