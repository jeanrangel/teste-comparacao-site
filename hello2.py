import urllib.request, os, time, csv, re
arquivoTexto1 = ""
arquivoTexto2 = ""
arquivoTextoFinal = ""
nomesAtributos = []

def reverteTexto(s):
    return s[::-1]

def escreverArquivoNoDisco():
    file = open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\" + nomeArquivo + ".html","w", encoding="utf-8")
    #write then close file
    #file.write('')
    file.write(str(arquivoTextoFinal))
    file.close()

def comitarNoGithub():
    os.system(r'cd C:/Users/jrangel\Documents/Python/GitHub & git add --all & git commit -am "Regular auto-commit $(timestamp)" & git push')
    print('esperando salvar...')
    time.sleep(5)

def abrirArquivoNomesAtributos():
    with open(r"C:\\Users\\jrangel\\Documents\\Python\\atributos.csv", "rt", encoding='ascii') as arquivoAtributos:
        leituraAtributos = csv.reader(arquivoAtributos)
        for row in leituraAtributos:
            nomesAtributos.append(row)

abrirArquivoNomesAtributos()
while True:
    with open(r"C:\\Users\\jrangel\\Documents\\Python\\links2.csv", "rt", encoding='ascii') as arquivoLinks:
        links = csv.reader(arquivoLinks)
        for row in links:
            print (row[0])
            arquivoTextoFinal = ''
            for atributo in nomesAtributos:
                with urllib.request.urlopen(row[0]) as f:
                    textoAtributo = atributo[0]
                    for line in f.readlines(): # iterate thru the lines
                        lineDecoded = line.decode('utf-8', 'ignore')
                        arquivoTexto1 = ''
                        arquivoTexto2 = ''
                        r = re.compile(textoAtributo)
                        for m in r.finditer(lineDecoded):
                            print(m.start())
                            for x in range(100):
                                if not x == 0:
                                    try:
                                        if m.start()-x > 0:
                                            caractereDaPosicao = lineDecoded[m.start()-x]
                                            arquivoTexto1 += caractereDaPosicao
                                    except:
                                        print("Fim da String")
                            for x in range(150):
                                if m.start()+x < len(lineDecoded):
                                    try:
                                        caractereDaPosicao = lineDecoded[m.start()+x]
                                        arquivoTexto2 += caractereDaPosicao
                                    except:
                                        print("Fim da String")
                            arquivoTexto2 += '\n'
                        arquivoTexto1 = reverteTexto(arquivoTexto1) 
                        arquivoTextoFinal += arquivoTexto1 + arquivoTexto2
            #open file with *.html* extension to write html
            nomeArquivo = row[0]
            nomeArquivo = nomeArquivo.replace(" ", "_")
            nomeArquivo = nomeArquivo.replace(".", "-")
            nomeArquivo = re.sub('[^a-zA-Z0-9_-]+', '', nomeArquivo)
            escreverArquivoNoDisco()
            comitarNoGithub()  