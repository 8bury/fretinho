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
    


def entercontinuar():
    input('\nPressione enter para continuar...\n')

opcoes = ['Buscar Endereço por CEP', 'Buscar CEP por endereço', 'Sair']

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
                        pprint.pprint(endereco)
                        entercontinuar()
                        break
                        #dps nois tira o break
            else:
                pprint.pprint(enderecospossiveis[1])
                entercontinuar()
    elif input_usuario == 3:
        loop = False
    else:
        print('\nDigite uma opção válida')
