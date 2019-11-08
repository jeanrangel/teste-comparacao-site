import urllib.request, os, time, csv, re
arquivoTextoAntesMatch = ""
arquivoTextoDepoisMatch = ""
arquivoTextoFinal = ""
textoAtributo = ""
arquivoTextoIntermediario = ""

nomesAtributos = []

def reverteTexto(s):
    return s[::-1]

def escreverArquivoNoDisco(nomeArquivo, arquivoTextoFinal):
    file = open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\" + nomeArquivo + ".html","w", encoding="utf-8")
    #write then close file
    #file.write('')
    file.write(str(arquivoTextoFinal))
    file.close()

def comitarNoGithub():
    os.system(r'cd C:/Users/jrangel\Documents/Python/GitHub & git add --all & git commit -am "Regular auto-commit $(timestamp)" & git push')
    print('Comitando...')
    time.sleep(4)
    
def abrirArquivoNomesAtributos():
    with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\atributos_desejados.csv", "rt", encoding='ascii') as arquivoAtributos:
        leituraAtributos = csv.reader(arquivoAtributos)
        for rowAtributo in leituraAtributos:
            nomesAtributos.append(rowAtributo)

def testeAbrirURL(linkPaginaAtual):
    return urllib.request.urlopen(linkPaginaAtual)

def abrirURLIterandoNoCodigo(linkPaginaAtual, textoAtributo):
    with urllib.request.urlopen(linkPaginaAtual) as f:
        for lineHTML in f.readlines(): # iterate thru the lines
            lineDecoded = lineHTML.decode('utf-8', 'ignore')
            global arquivoTextoAntesMatch
            global arquivoTextoDepoisMatch
            global arquivoTextoIntermediario
            arquivoTextoAntesMatch = ''
            arquivoTextoDepoisMatch = ''
            arquivoTextoIntermediario = ''
            iteradorMatches = 1
            r = re.compile(textoAtributo)
            regexp = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
            regexEndOfLine = re.compile(r"[\r\n]")
            #Somente prossegue se a linha tiver alguma coisa
            if regexp.search(lineDecoded):
                matchesNaLinha = r.finditer(lineDecoded)
                quantiaDeMatchesNaLinha = len( [m for m in r.finditer(lineDecoded) ] )
                for m in matchesNaLinha:
                    #Iteracao pra tras
                    for x in range(60):
                        #Ignora a posicao zero da linha, jah que sera englobada no proximo for
                        if not x == 0:
                            try:
                                #Vai de elemento em elemento ate o comeco da linha (chegar no elm zero)
                                if m.start()-x >= 0:
                                    caractereDaPosicao = lineDecoded[m.start()-x]
                                    arquivoTextoAntesMatch += caractereDaPosicao
                            except:
                                print("Fim da String")
                    #Iteracao para frente de onde encontrou o match
                    for x in range(150):
                        #Percorre a linha para frente ate chegar no final dela (length da linha)
                        if m.start()+x < len(lineDecoded):
                            try:
                                caractereDaPosicao = lineDecoded[m.start()+x]
                                if regexEndOfLine.search(caractereDaPosicao):
                                    break  
                                else: 
                                    arquivoTextoDepoisMatch += caractereDaPosicao    
                            except:
                                print("Fim da String")
                        
                    if iteradorMatches >= quantiaDeMatchesNaLinha:
                        arquivoTextoDepoisMatch += '\n'
                    iteradorMatches += 1
                    arquivoTextoAntesMatch = reverteTexto(arquivoTextoAntesMatch) 
                    arquivoTextoDepoisMatch = arquivoTextoAntesMatch + arquivoTextoDepoisMatch
                    arquivoTextoAntesMatch = ''
                    arquivoTextoIntermediario += arquivoTextoDepoisMatch
                    arquivoTextoDepoisMatch = ''

            #Como a String foi feita indo de elemento em elemento de tras pra frente, esta ao contrario
            global arquivoTextoFinal
            #Verificar se pelo menos um dos "lados" nao possui somente vazio para salvar em disco
            if regexp.search(arquivoTextoIntermediario):    
                arquivoTextoFinal += arquivoTextoIntermediario
            
def mainSalvarArquivo():
    while True:
        with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\links_para_salvar.csv", "rt", encoding='ascii') as arquivoLinks:
            links = csv.reader(arquivoLinks)
            for rowLink in links:
                #Booleando que indica que se, caso consiga acessar a URL, pode escrever no arquivo e comitar
                
                ###### Zerando as variáveis ######
                global arquivoTextoFinal
                arquivoTextoFinal = ''
                deveProsseguir = False
                ##################################

                linkPaginaAtual = rowLink[0]
                print ('Pagina que esta sendo trabalhada no momento: ' + linkPaginaAtual)
                for atributo in nomesAtributos: 
                    textoAtributo = atributo[0]  
                    for contadorTent in range(5):
                        try:
                            testeAbrirURL(linkPaginaAtual)
                            deveProsseguir = True
                            break
                        except:
                            print('Erro ao acessar a pagina. Tentando novamente em 5 segundos. Tentativa: ' + str(contadorTent))
                            time.sleep(0.5) 
                if deveProsseguir:   
                    abrirURLIterandoNoCodigo(linkPaginaAtual, textoAtributo)  

                    regexp = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
                    #Somente prossegue se a linha tiver alguma coisa
                    if regexp.search(arquivoTextoFinal):
                        #open file with *.html* extension to write html
                        nomeArquivo = rowLink[0]
                        nomeArquivo = nomeArquivo.replace(" ", "_")
                        nomeArquivo = nomeArquivo.replace(".", "-")
                        nomeArquivo = re.sub('[^a-zA-Z0-9_-]+', '', nomeArquivo)
                        escreverArquivoNoDisco(nomeArquivo, arquivoTextoFinal)
                        time.sleep(1)
                        comitarNoGithub()
        print('Passando o tempo... Esperando o proximo dia')
        #Aqui a quantia de segundos vai refletir a passagem de um dia completo (24 horas) 
        time.sleep(5)
###### METODO MAIN ######
abrirArquivoNomesAtributos()
mainSalvarArquivo() 