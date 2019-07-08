# Abertura de Ordens de Serviço

Código simples (específico) para ajudar fiscais durante a abertura de ordens de serviço diretamente no ERP.

----
## Antes de começar...
Certifique-se que o [GIT](https://git-scm.com/downloads) está instalado em seu PC. Proceda baixando o código fonte:

    $ git clone https://github.com/igorccouto/abertura_de_ordens_de_servico
    $ cd abertura_de_ordens_de_servico

### Config
1. Baixe e instale o [Python 3.6.1](https://www.python.org/downloads/release/python-361).
    1. Testado no Windows 10 - 64 bits.

2. Baixe e instale o [Google Chrome](https://www.google.com/intl/pt-BR/chrome).

3. Baixe o [ChromeDriver](http://chromedriver.chromium.org/downloads).
    1. Escolha de acordo com a versão do Google Chrome instalado no seu PC.
    2. Renomeie o executável para *chromedriver.exe* e salve-o dentro de uma pasta chamada *chromedriver* no diretório raiz.

4. Para instalar a bibliotecas, dentro da pasta raiz, execute:

        $ pip install -r requirements.txt

### Arquivos de entrada

#### **.env**

No diretório raiz, crie um arquivo chamado *.env* com as seguintes variáveis:

- USUARIO=*SEU NOME DE USUARIO*
- SENHA=*SUA SENHA*
- EMAIL=*SEU EMAIL*
- CODIGO\_ANS\_FISCAL=*SEU CODIGO ANS*

> **Por motivos de segurança, altere as permissões deste arquivo para que somente a sua conta tenha acesso.**

Não use aspas, colchetes ou qualquer caractere para delimitar as variáveis. Veja um modelo deste arquivo em [exemplos](https://github.com/igorccouto/abertura_de_ordens_de_servico/tree/master/exemplos).

#### **ordens\_de\_servico.csv**

No diretório raiz, crie um arquivo chamado *ordens\_de\_servico.csv* contendo as informações das ordens de serviço que você deseja abrir. Veja um modelo deste arquivo em [exemplos](https://github.com/igorccouto/abertura_de_ordens_de_servico/tree/master/exemplos).

----
## Uso
Após as configurações iniciais, no diretório raiz, execute:

    $ python .\src\executa.py

O código irá abrir um navegador e utilizará as informações em *ordens\_de\_servico.csv* para para abrir as ordens de serviço sequencialmente. 

### Arquivo de saída
Após cada interação, o código atualiza o arquivo **ordens\_de\_servico\_abertas.csv**. Neste arquivo, estão os registros das ordens de serviço abertas anteriormente.
> Para manter um registro, evite apagá-lo.