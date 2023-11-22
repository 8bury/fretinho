import requests
import pprint
import pandas as pd
loop = True

def pedir_endereço(cep):
    link = f'https://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link)
    print(requisicao)
    if requisicao.status_code == 200:
        return requisicao.json()

def pedir_cep(uf, localidade, logradouro):
    link = f'https://viacep.com.br/ws/{uf}/{localidade}/{logradouro}/json/'
    requisicao = requests.get(link)
    print(requisicao)
    if requisicao.status_code == 200:
        return requisicao.json()
    else:
        return {'erro': 'True'}
    
def calculardistanciatempo(cep1, cep2):

    api_file = open('apikey.txt', 'r')
    api_key = api_file.read()
    api_file.close()

    link = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
    requisicao = requests.get(link + '&origins=' + cep1 + '&destinations=' + cep2 + '&key=' + api_key)
    if 'ZERO_RESULTS' in requisicao.json()['rows'][0]['elements'][0]['status'] or 'NOT_FOUND' in requisicao.json()['rows'][0]['elements'][0]['status']:
        return 'erro', 'erro'
    else:
        tempo = requisicao.json()['rows'][0]['elements'][0]['duration']['value']
        tempotext = requisicao.json()['rows'][0]['elements'][0]['duration']['text']
        #emsegundos
        
        distancia = requisicao.json()['rows'][0]['elements'][0]['distance']['value']
        distanciatext = requisicao.json()['rows'][0]['elements'][0]['distance']['text']
        #emmetros
        return tempo, distancia, tempotext, distanciatext

def entercontinuar():
    input('\nPressione enter para continuar...\n')

opcoes = ['Buscar Endereço por CEP', 'Buscar CEP por endereço', 'Calcular Frete', 'Sair']

bairro = ''
while loop:
    for i in range(len(opcoes)):
        print(f'{i+1} - {opcoes[i]}')
    input_usuario = int(input('\nDigite a opção desejada: '))
    if input_usuario == 1:
        cep = input('Digite o CEP: ')
        while cep.isdigit() == False or len(cep) != 8:
            cep = input('Digite o CEP (Somente números): ')
        informaçoesendereço = pedir_endereço(cep)

        if 'erro' in informaçoesendereço:
            print('CEP inválido')
            entercontinuar()
            continue
        else:
            print('\nInformações do endereço:')
            print(f'\nCEP : {informaçoesendereço["cep"]}')
            print(f'Rua : {informaçoesendereço['logradouro']}')
            print(f'Bairro : {informaçoesendereço['bairro']}')
            print(f'Cidade : {informaçoesendereço['localidade']}')
            print(f'Estado : {informaçoesendereço['uf']}')
            entercontinuar()
        
    elif input_usuario == 2:
        estado = (input('Digite o estado (ABREVIADO): '))
        while len(estado) != 2:
            estado = (input('Digite o estado (ABREVIADO): '))
        cidade = (input('Digite a cidade (NOMECOMPLETO): '))
        rua = (input('Digite a rua: '))
        bairro = (input('Digite o bairro (OPCIONAL): ')).capitalize()

        enderecospossiveis = pedir_cep(estado, cidade, rua)
        if 'erro' in enderecospossiveis or len(enderecospossiveis) == 0:
            print('Endereço inválido')
        else:
            if bairro != '':
                for endereco in enderecospossiveis:
                    if bairro in endereco['bairro']:
                        print(f'\nCEP: {endereco["cep"]}')
                        print(f'Rua: {endereco["logradouro"]}')
                        print(f'Bairro: {endereco["bairro"]}')
                        print(f'Cidade: {endereco["localidade"]}')
                        print(f'Estado: {endereco["uf"]}')
                        entercontinuar()
                        break
                        #dps nois tira o break
            else:
                print(f'\nCEP: {enderecospossiveis[0]["cep"]}')
                print(f'Rua: {enderecospossiveis[0]["logradouro"]}')
                print(f'Bairro: {enderecospossiveis[0]["bairro"]}')
                print(f'Cidade: {enderecospossiveis[0]["localidade"]}')
                print(f'Estado: {enderecospossiveis[0]["uf"]}')

                entercontinuar()
    elif input_usuario == 3:
        cep1 = input('Digite o CEP ou endereço de origem: ')
        cep2 = input('Digite o CEP ou endereço de destino: ')
        tempo, distancia, tempotext, distanciatext = calculardistanciatempo(cep1, cep2)
        print(tempo, distancia)
        if tempo and distancia == 'erro':
            print('Erro ao calcular a distância ou tempo, tente novamente.')
            entercontinuar()
            continue
        else:
            dimensões= input('Digite as dimensões do produto em centímetros e considere quilos para o peso (Largura, Altura, Comprimento, Peso): ').split(',')
            largura = float(dimensões[0])
            altura = float(dimensões[1])
            comprimento = float(dimensões[2])
            peso = float(dimensões[3])
            volume = largura * altura * comprimento
            frete = 10
            #acima de 2 metroscubicos, o valor fica maior
            if distancia < 80000:
                frete += 0.0005 * distancia
            elif distancia < 200000:
                frete += 0.0002 * distancia
            else:
                frete += 0.000025 * distancia
            if volume > 1000000:
                #se for maior que 1 metros cubicos, o valor do frete aumenta
                #para cada 1000cm cubicos ou 0,0001 metrocubicos, o valor do frete aumenta 1 real
                frete += (volume-1000000)*0.0001
            if peso > 10:
                #se for maior que 10kg, o valor do frete aumenta
                #para cada 1kg, o valor do frete aumenta 50 centavos
                frete += (peso-10)/2
            print(f'\nDistância: {distanciatext}')
            print(f'volume: {volume/1000000} metros cúbicos')
            print(f'\nTempo estimado para entrega: {tempotext}')
            print(f'Frete estimado: R$ {frete}')
            entercontinuar()
    elif input_usuario == 4:
        loop = False
    else:
        print('\nDigite uma opção válida')
