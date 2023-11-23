import requests
import pprint
loop = True

def pedir_endereço(cep):
    link = f'https://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link)
    if requisicao.status_code == 200:
        return requisicao.json()

def pedir_cep(uf, localidade, logradouro):
    link = f'https://viacep.com.br/ws/{uf}/{localidade}/{logradouro}/json/'
    requisicao = requests.get(link)
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

def dimensoes():

    dimensões = input('Digite as dimensões do produto em centímetros e considere quilos para o peso (Largura, Altura, Comprimento, Peso): ').split(',')
    largura = float(dimensões[0])
    altura = float(dimensões[1])
    comprimento = float(dimensões[2])
    peso = float(dimensões[3])
    volume = largura * altura * comprimento

    return largura, altura, comprimento, peso, volume

def calculafrete(volume, distancia, peso):

    frete = 10

    if distancia < 80000:
        frete += 0.0005 * distancia
    elif distancia < 200000:
        frete += 0.0002 * distancia
    else:
        frete += 0.000025 * distancia
    if volume > 1000000:
        #se for maior que 1 metros cubicos, o valor do frete aumenta
        #para cada 1 litro o valor do frete aumenta 1 real
        frete += (volume-1000000)*0.0001
    if peso > 10:
        #se for maior que 10kg, o valor do frete aumenta
        #para cada 1kg, o valor do frete aumenta 50 centavos
        frete += (peso-10)/2
    return frete

def printar_endereço(endereço):
    print(f'\nCEP : {endereço["cep"]}')
    print(f'Rua : {endereço["logradouro"]}')
    print(f'Bairro : {endereço["bairro"]}')
    print(f'Cidade : {endereço["localidade"]}')
    print(f'Estado : {endereço["uf"]}')

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
            printar_endereço(informaçoesendereço)
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
                endereco_encontrado = False
                for endereco in enderecospossiveis:
                    if bairro in endereco['bairro']:
                        printar_endereço(endereco)
                        entercontinuar()
                        endereco_encontrado = True
                if not endereco_encontrado:
                    print('\nEndereço com o bairro especificado não encontrado')
                    entercontinuar()

            else:
                printar_endereço(enderecospossiveis[0])
                entercontinuar()
    elif input_usuario == 3:
        cep1 = input('Digite o CEP ou endereço de origem: ')
        cep2 = input('Digite o CEP ou endereço de destino: ')
        tempo, distancia, tempotext, distanciatext = calculardistanciatempo(cep1, cep2)
        if tempo and distancia == 'erro':
            print('Erro ao calcular a distância ou tempo, tente novamente.')
            entercontinuar()
            continue
        else:
            
            largura, altura, comprimento, peso, volume = dimensoes()
            frete = calculafrete(volume, distancia, peso)
            
            print(f'\nDistância: {distanciatext}')
            print(f'volume: {volume/1000000} metros cúbicos')
            print(f'Tempo estimado para entrega: {tempotext}')
            print(f'Frete estimado: R$ {frete}')
            entercontinuar()
    elif input_usuario == 4:
        loop = False
    else:
        print('\nDigite uma opção válida')