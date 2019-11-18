import urllib.request, os, time, csv, re, datetime
nomes_atributos = []
texto_atributo = ''


dt = datetime.datetime.today()
arquivo_texto_antes_match  = ''
arquivo_texto_depois_match = ''
arquivo_texto_final = ''

arquivo_texto_intermediario = ''
data_do_commit = ''

global deve_prosseguir
deve_prosseguir = False

#Esta funcao somente inverte a linha de texto, pois ela foi criada sendo adicionados elementos de tras para frente.
def reverte_texto(s):
    return s[::-1]

def escrever_arquivo_no_disco(nome_arquivo, arquivo_texto_final):
    file = open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\" + nome_arquivo + ".html","w", encoding="utf-8")
    file.write(str(arquivo_texto_final))
    file.close()

def comitar_no_github(data_do_commit):
    os.system(r'cd C:/Users/jrangel\Documents/Python/GitHub & git add --all & git commit -am '
                '"Atenção! Houve mudança no site no dia: ' + data_do_commit + '. Favor, conferir alterações '
                'clicando no link deste email." & git push')
    print('______________________________________________________________')
    print('Se houver algo para comitar, comando executado.')
    print('______________________________________________________________')
    time.sleep(4)
    
def abrir_arquivo_nomes_atributos():
    with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\atributos_desejados.csv", 
                "rt", encoding='ascii') as arquivo_atributos:
        leitura_atributos = csv.reader(arquivo_atributos)
        #Vai abrir o CSV que contem uma linha para cada atributo desejado. Ele podera ser qualquer String que desejamos
        # procurar no documento HTML. Exemplo: "data-ic-" vai englobar tanto "data-ic-trigger" quanto "data-ic-section".
        for row_atributo in leitura_atributos:
            nomes_atributos.append(row_atributo)

def teste_abrir_URL(link_pagina_atual):
    return urllib.request.urlopen(link_pagina_atual)

def verificar_se_URL_esta_valida(link_pagina_atual):
    #Metodo auto explicativo e de facil compreensao. Como ele retorna um booleano, preenche o valor no main
    # indicando se deve continuar o codigo. Este metodo impede o codigo de travar caso a URL esteja indisponvel 
    # por qualquer razao (por exemplo, esta fora do ar).
    for contador_tent in range(5):
        try:
            teste_abrir_URL(link_pagina_atual)
            return True
        except:
            print('!!! - Erro ao acessar a pagina: -- ' + link_pagina_atual + ' -- Tentando novamente em 5 segundos.'
            ' Tentativa: ' + str(contador_tent))
            time.sleep(0.1) 
            if contador_tent >= 4:
                return False

def abrir_URL_iterando_no_codigo(link_pagina_atual, texto_atributo):
    with urllib.request.urlopen(link_pagina_atual) as f:
        for lineHTML in f.readlines(): # Itera pelas linhas do documento HTML.
            linha_decodificada = lineHTML.decode('utf-8', 'ignore')

            ###### Resetando as variáveis ######
            global arquivo_texto_antes_match
            global arquivo_texto_depois_match
            global arquivo_texto_intermediario
            global arquivo_texto_final
            arquivo_texto_antes_match = ''
            arquivo_texto_depois_match = ''
            arquivo_texto_intermediario = ''
            iterador_matches = 1
            ##################################

            r = re.compile(texto_atributo)
            regex_qualquer_caractere = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
            regex_fim_da_linha = re.compile(r"[\r\n]")
            #Somente prossegue se a linha tiver alguma coisa.
            if regex_qualquer_caractere.search(linha_decodificada):
                matches_na_linha = r.finditer(linha_decodificada)
                #Forma ruim encontrada para contar quantas ocorrencias foram encontradas na linha
                # isto eh importante para sabermos se a linha chegou ao fim.
                quantia_de_matches_na_linha = len( [m for m in r.finditer(linha_decodificada) ] )
                for m in matches_na_linha:
                    #Iteracao pra tras.
                    for x in range(60):
                        #Ignora a posicao zero da linha, jah que sera englobada no proximo for.
                        if not x == 0:
                            try:
                                #Vai de elemento em elemento ate o comeco da linha (chegar no elm zero).
                                if m.start()-x >= 0:
                                    #-x significa que esta indo para tras.
                                    caractere_da_posicao = linha_decodificada[m.start()-x]
                                    arquivo_texto_antes_match += caractere_da_posicao
                            except:
                                None
                    #Iteracao para frente de onde encontrou o match. Inclui o elemento zero.
                    for x in range(150):
                        #Percorre a linha para frente ate chegar no final dela (length da linha).
                        if m.start()+x < len(linha_decodificada):
                            try:
                                #+x significa que esta indo para frente.
                                caractere_da_posicao = linha_decodificada[m.start()+x]
                                #Caso o caractere atual de Regex com o final da linha, termina o for.
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
                    #Como a String foi feita indo de elemento em elemento de tras pra frente, esta ao contrario.
                    arquivo_texto_depois_match = arquivo_texto_antes_match + arquivo_texto_depois_match
                    arquivo_texto_antes_match = ''
                    arquivo_texto_intermediario += arquivo_texto_depois_match
                    arquivo_texto_depois_match = ''
            #Verificar se pelo nao possui somente vazio para salvar em disco.
            if regex_qualquer_caractere.search(arquivo_texto_intermediario):    
                arquivo_texto_final += arquivo_texto_intermediario
        
def main():
    while True:
        abrir_arquivo_nomes_atributos()
        #Em cada iteracao, pega a data atual no formato brasileiro. Diminui um dia, pois provavelmente o site foi alterado no dia anterior.
        data_do_commit = 'Dia: ' + str(dt.day-1) + '/' + str(dt.month) + '/' + str(dt.year)
        print(data_do_commit)
        with open(r"C:\\Users\\jrangel\\Documents\\Python\\GitHub\\arquivos_necessarios\\links_para_salvar.csv", "rt", encoding='ascii') as arquivo_links:
            #Abre arquivo CSV que possui um link para cada linha. O codigo vai iterar por todos os links.
            links = csv.reader(arquivo_links)
            for row_link in links:

                ###### Zerando as variáveis ######
                global arquivo_texto_final
                arquivo_texto_final = ''
               # deve_prosseguir = False
                ##################################

                link_pagina_atual = row_link[0]
                print('______________________________________________________________')
                print ('Pagina que esta sendo trabalhada no momento: ' + link_pagina_atual)
                print('______________________________________________________________')
                for atributo in nomes_atributos: 
                    texto_atributo = atributo[0]  
                    deve_prosseguir = verificar_se_URL_esta_valida(link_pagina_atual)
                    if not deve_prosseguir:
                        #Se nao eh possivel abrir o link, quebra o for e sai para o proximo endereco URL.
                        break
                    
                if deve_prosseguir:  
                    print('______________________________________________________________')
                    print('Executando o processo para verificar se houve mudanca no HTML.') 
                    print('______________________________________________________________')
                    abrir_URL_iterando_no_codigo(link_pagina_atual, texto_atributo)  
                    regex_qualquer_caractere = re.compile(r'[a-zA-Z/<>[\]{}0-9]')
                    #Somente prossegue se a linha tiver alguma coisa.
                    if regex_qualquer_caractere.search(arquivo_texto_final):
                        #Cria o arquivo HTML com o mesmo nome da paginaopen file with *.html* extension to write html
                        nome_arquivo = row_link[0]
                        nome_arquivo = nome_arquivo.replace(" ", "_")
                        nome_arquivo = nome_arquivo.replace(".", "+")
                        nome_arquivo = re.sub('[^a-zA-Z0-9+_-]+', '', nome_arquivo)
                        escrever_arquivo_no_disco(nome_arquivo, arquivo_texto_final)
                        time.sleep(1)
                        comitar_no_github(data_do_commit)
            print('*********************************************************************************')    
            print('Passando o tempo... Esperando o proximo dia')
            print('*********************************************************************************')    
            #Aqui a quantia de segundos vai refletir a passagem de um dia completo (24 horas) 
            time.sleep(5)

if __name__ == "__main__":
    main()