import urllib.request, os, time, csv, re
arquivo_texto_antes_match  = ''
arquivo_texto_depois_match = ''
arquivo_texto_final = ''
texto_atributo = ''
arquivo_texto_intermediario = ''
global deve_prosseguir
deve_prosseguir = False

nomes_atributos = []

def reverte_texto(s):
    return s[::-1]

def escrever_arquivo_no_disco(nome_arquivo, arquivo_texto_final):
    file = open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\" + nome_arquivo + ".html","w", encoding="utf-8")
    #write then close file
    #file.write('')
    file.write(str(arquivo_texto_final))
    file.close()

def comitar_no_github():
    os.system(r'cd C:/Users/jrangel\Documents/Python/GitHub & git add --all & git commit -am "Regular auto-commit $(timestamp)" & git push')
    print('Se houver algo para comitar, comando executado.')
    time.sleep(4)
    
def abrir_arquivo_nomes_atributos():
    with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\atributos_desejados.csv", "rt", encoding='ascii') as arquivo_atributos:
        leitura_atributos = csv.reader(arquivo_atributos)
        for row_atributo in leitura_atributos:
            nomes_atributos.append(row_atributo)

def teste_abrir_URL(link_pagina_atual):
    return urllib.request.urlopen(link_pagina_atual)

def verificar_se_URL_esta_valida(link_pagina_atual):
    for contador_tent in range(5):
        try:
            teste_abrir_URL(link_pagina_atual)
            return True
        except:
            print('Erro ao acessar a pagina: -- ' + link_pagina_atual + ' -- Tentando novamente em 5 segundos. Tentativa: ' + str(contador_tent))
            time.sleep(0.5) 
            if contador_tent >= 4:
                return False

def abrir_URL_iterando_no_codigo(link_pagina_atual, texto_atributo):
    with urllib.request.urlopen(link_pagina_atual) as f:
        for lineHTML in f.readlines(): # iterate thru the lines
            linha_decodificada = lineHTML.decode('utf-8', 'ignore')
            global arquivo_texto_antes_match
            global arquivo_texto_depois_match
            global arquivo_texto_intermediario
            arquivo_texto_antes_match = ''
            arquivo_texto_depois_match = ''
            arquivo_texto_intermediario = ''
            iterador_matches = 1
            r = re.compile(texto_atributo)
            regexp = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
            regex_fim_da_linha = re.compile(r"[\r\n]")
            #Somente prossegue se a linha tiver alguma coisa
            if regexp.search(linha_decodificada):
                matches_na_linha = r.finditer(linha_decodificada)
                quantia_de_matches_na_linha = len( [m for m in r.finditer(linha_decodificada) ] )
                for m in matches_na_linha:
                    #Iteracao pra tras
                    for x in range(60):
                        #Ignora a posicao zero da linha, jah que sera englobada no proximo for
                        if not x == 0:
                            try:
                                #Vai de elemento em elemento ate o comeco da linha (chegar no elm zero)
                                if m.start()-x >= 0:
                                    caractere_da_posicao = linha_decodificada[m.start()-x]
                                    arquivo_texto_antes_match += caractere_da_posicao
                            except:
                                None
                    #Iteracao para frente de onde encontrou o match
                    for x in range(150):
                        #Percorre a linha para frente ate chegar no final dela (length da linha)
                        if m.start()+x < len(linha_decodificada):
                            try:
                                caractere_da_posicao = linha_decodificada[m.start()+x]
                                if regex_fim_da_linha.search(caractere_da_posicao):
                                    break  
                                else: 
                                    arquivo_texto_depois_match += caractere_da_posicao    
                            except:
                                None
                    if iterador_matches >= quantia_de_matches_na_linha:
                        arquivo_texto_depois_match += '\n'
                    iterador_matches += 1
                    arquivo_texto_antes_match = reverte_texto(arquivo_texto_antes_match) 
                    arquivo_texto_depois_match = arquivo_texto_antes_match + arquivo_texto_depois_match
                    arquivo_texto_antes_match = ''
                    arquivo_texto_intermediario += arquivo_texto_depois_match
                    arquivo_texto_depois_match = ''

            #Como a String foi feita indo de elemento em elemento de tras pra frente, esta ao contrario
            global arquivo_texto_final
            #Verificar se pelo menos um dos "lados" nao possui somente vazio para salvar em disco
            if regexp.search(arquivo_texto_intermediario):    
                arquivo_texto_final += arquivo_texto_intermediario
        
def main():
    while True:
        abrir_arquivo_nomes_atributos()
        with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\links_para_salvar.csv", "rt", encoding='ascii') as arquivo_links:
            links = csv.reader(arquivo_links)
            for row_link in links:
                #Booleando que indica que se, caso consiga acessar a URL, pode escrever no arquivo e comitar
                
                ###### Zerando as variáveis ######
                global arquivo_texto_final
                arquivo_texto_final = ''
               # deve_prosseguir = False
                ##################################

                link_pagina_atual = row_link[0]
                print ('Pagina que esta sendo trabalhada no momento: ' + link_pagina_atual)
                for atributo in nomes_atributos: 
                    texto_atributo = atributo[0]  
                    deve_prosseguir = verificar_se_URL_esta_valida(link_pagina_atual)
                    if not deve_prosseguir:
                        break
                    
                if deve_prosseguir:  
                    print('Executando o processo para verificar se houve mudanca no HTML.') 
                    abrir_URL_iterando_no_codigo(link_pagina_atual, texto_atributo)  
                    regexp = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
                    #Somente prossegue se a linha tiver alguma coisa
                    if regexp.search(arquivo_texto_final):
                        #open file with *.html* extension to write html
                        nome_arquivo = row_link[0]
                        nome_arquivo = nome_arquivo.replace(" ", "_")
                        nome_arquivo = nome_arquivo.replace(".", "-")
                        nome_arquivo = re.sub('[^a-zA-Z0-9_-]+', '', nome_arquivo)
                        escrever_arquivo_no_disco(nome_arquivo, arquivo_texto_final)
                        time.sleep(1)
                        comitar_no_github()
                
            print('Passando o tempo... Esperando o proximo dia')
            #Aqui a quantia de segundos vai refletir a passagem de um dia completo (24 horas) 
            time.sleep(5)

if __name__ == "__main__":
    main()