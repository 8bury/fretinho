#importar bibliotecas
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk # utilizados para importar a imagem da web
import requests
from io import BytesIO

def pedir_endereço(cep):
    if len(cep) != 8 or cep.isdigit() == False:
        messagebox.showerror('Erro', 'CEP inválido')
    else:
        link = f'https://viacep.com.br/ws/{cep}/json/'
        requisicao = requests.get(link)
        if requisicao.status_code == 200:
            informaçoesendereço = requisicao.json()
            if 'erro' in informaçoesendereço:
                messagebox.showerror('Erro', 'CEP não encontrado')
            else:
                printar_endereço(informaçoesendereço)
        else:
            messagebox.showerror('Erro', 'CEP não encontrado')

def pedir_cep(uf, localidade, logradouro, bairro):
    if uf == '' or localidade == '' or logradouro == '':
        messagebox.showerror('Erro', 'Preencha todos os campos')
    else:
        link = f'https://viacep.com.br/ws/{uf}/{localidade}/{logradouro}/json/'
        requisicao = requests.get(link)
        if requisicao.status_code == 200:
            enderecospossiveis = requisicao.json()
            if 'erro' in enderecospossiveis or len(enderecospossiveis) == 0:
                messagebox.showerror('Erro', 'Endereço não encontrado')
            else:
                if bairro != '':
                    endereco_encontrado = False
                    for endereco in enderecospossiveis:
                        if bairro.upper() in endereco['bairro'].upper():
                            printar_endereço(endereco)
                            
                            endereco_encontrado = True
                    if not endereco_encontrado:
                        messagebox.showerror('Erro', 'Endereço com o bairro especificado não encontrado')
                else:
                    printar_endereço(enderecospossiveis[0])  
        else:
            messagebox.showerror('Erro', 'Endereço não encontrado')
    
def calcularfrete(cep1, cep2, largura, altura, comprimento, peso):
    if largura.isdigit() == False or altura.isdigit() == False or comprimento.isdigit() == False or peso.isdigit() == False:
        messagebox.showerror('Erro', 'Dimensões inválidas')
    else:
        largura = float(largura)
        altura = float(altura)
        comprimento = float(comprimento)
        peso = float(peso)
        volume = largura * altura * comprimento
        api_file = open('apikey.txt', 'r')
        api_key = api_file.read()
        api_file.close()

        link = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
        requisicao = requests.get(link + '&origins=' + cep1 + '&destinations=' + cep2 + '&key=' + api_key)
        if 'ZERO_RESULTS' in requisicao.json()['rows'][0]['elements'][0]['status'] or 'NOT_FOUND' in requisicao.json()['rows'][0]['elements'][0]['status']:
            messagebox.showerror('Erro', 'CEP não encontrado')
            return
        else:
            tempo = requisicao.json()['rows'][0]['elements'][0]['duration']['value']
            tempotext = requisicao.json()['rows'][0]['elements'][0]['duration']['text']
            #emsegundos

            distancia = requisicao.json()['rows'][0]['elements'][0]['distance']['value']
            distanciatext = requisicao.json()['rows'][0]['elements'][0]['distance']['text']
            #emmetros

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
            textofrete['text'] = f'Frete: R${frete:.2f}\nTempo: {tempotext}\nDistância: {distanciatext}'

def printar_endereço(endereço):
    cep = endereço['cep']
    rua = endereço['logradouro']
    bairro = endereço['bairro']
    cidade = endereço['localidade']
    estado = endereço['uf']
    
    texto = f'CEP : {cep}\nRua : {rua}\nBairro : {bairro}\nCidade : {cidade}\nEstado : {estado}'
    textoendereço['text'] = texto


#VARIAVÉL TEMPORÁRIA, APENAS PARA TESTAR O TESTE DE VERIFICAÇÃO E UTILIZAR O BOTÃO DE FAZER LOGIN.
#tanto para ler como para escrever no arquivo, é necessário abrir o arquivo com o modo de leitura ou escrita.
with open('usuarios.txt', 'r') as usuarios_file:
    usuarios = usuarios_file.read()
    transformar_em_dicionario = eval(usuarios)
if type(transformar_em_dicionario) == dict:
    usuarios = transformar_em_dicionario
else:
    usuarios = {}
    messagebox.showerror('Erro', 'Arquivo de usuários corrompido')


#FUNÇÃO PARA FAZER LOGIN, COMPARANDO OS DADOS DIGITADOS COM OS DADOS DO DICIONÁRIO USUARIOS.
def fazer_login(nivel_acesso):
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    
    if usuario in usuarios and usuarios[usuario]['senha'] == senha and usuarios[usuario]['nivel_acesso'] == nivel_acesso:
        print(f"Usuário autenticado: {usuario}, Nível de Acesso: {nivel_acesso}")
        abrir_tela2(nivel_acesso)
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos")
def opcao1tela():
    global textoendereço
    tela2.withdraw()
    tela3 = tk.Toplevel(tela2)
    tela3.resizable(False, False)
    tela3.title("FRETINHO")
    tela3.geometry("600x600")
    label = tk.Label(tela3, text="Buscar Endereço por CEP", font=("Arial", 30))
    label.pack(pady=5, padx=5)
    label_cep = tk.Label(tela3, text="CEP:", font=("Arial", 10))
    label_cep.pack(pady=5, padx=5)
    entry_cep = tk.Entry(tela3, font=("Arial", 10))
    entry_cep.pack(pady=5, padx=5)
    botao_buscar = tk.Button(tela3, text="Buscar", font=("Arial", 10), width=10, command=lambda: pedir_endereço(entry_cep.get()))
    botao_buscar.pack(pady=5, padx=5)
    botao_voltar = tk.Button(tela3, text="Voltar", font=("Arial", 10), width=10, command=lambda: (tela3.destroy(), tela2.deiconify()))
    botao_voltar.pack(pady=5, padx=5)
    textoendereço = tk.Label(tela3, text='')
    textoendereço.pack(pady=5, padx=5)
def opcao2tela():
    global textoendereço
    tela2.withdraw()
    tela3 = tk.Toplevel(tela2)
    tela3.resizable(False, False)
    tela3.title("FRETINHO")
    tela3.geometry("600x600")
    label = tk.Label(tela3, text="Buscar CEP por endereço", font=("Arial", 30))
    label.pack(pady=5, padx=5)
    label_uf = tk.Label(tela3, text="UF (abreviado):", font=("Arial", 10))
    label_uf.pack(pady=5, padx=5)
    entry_uf = tk.Entry(tela3, font=("Arial", 10))
    entry_uf.pack(pady=5, padx=5)
    label_cidade = tk.Label(tela3, text="Cidade (nome completo):", font=("Arial", 10))
    label_cidade.pack(pady=5, padx=5)
    entry_cidade = tk.Entry(tela3, font=("Arial", 10))
    entry_cidade.pack(pady=5, padx=5)
    label_rua = tk.Label(tela3, text="Rua:", font=("Arial", 10))
    label_rua.pack(pady=5, padx=5)
    entry_rua = tk.Entry(tela3, font=("Arial", 10))
    entry_rua.pack(pady=5, padx=5)
    label_bairro = tk.Label(tela3, text="Bairro (OPCIONAL):", font=("Arial", 10))
    label_bairro.pack(pady=5, padx=5)
    entry_bairro = tk.Entry(tela3, font=("Arial", 10))
    entry_bairro.pack(pady=5, padx=5)
    botao_buscar = tk.Button(tela3, text="Buscar", font=("Arial", 10), width=10, command=lambda: pedir_cep(entry_uf.get(), entry_cidade.get(), entry_rua.get(), entry_bairro.get()))
    botao_buscar.pack(pady=5, padx=5)
    botao_voltar = tk.Button(tela3, text="Voltar", font=("Arial", 10), width=10, command=lambda: (tela3.destroy(), tela2.deiconify()))
    botao_voltar.pack(pady=5, padx=5)
    textoendereço = tk.Label(tela3, text='')
    textoendereço.pack(pady=5, padx=5)
def opcao3tela():
    global textofrete
    tela2.withdraw()
    tela3 = tk.Toplevel(tela2)
    tela3.resizable(False, False)
    tela3.title("FRETINHO")
    tela3.geometry("600x800")
    label = tk.Label(tela3, text="Calcular Frete", font=("Arial", 30))
    label.pack(pady=5, padx=5)
    label_cep1 = tk.Label(tela3, text="CEP  ou endereço de origem:", font=("Arial", 10))
    label_cep1.pack(pady=5, padx=5)
    entry_cep1 = tk.Entry(tela3, font=("Arial", 10))
    entry_cep1.pack(pady=5, padx=5)
    label_cep2 = tk.Label(tela3, text="CEP ou endereço de destino:", font=("Arial", 10))
    label_cep2.pack(pady=5, padx=5)
    entry_cep2 = tk.Entry(tela3, font=("Arial", 10))
    entry_cep2.pack(pady=5, padx=5)
    label_dimensoes = tk.Label(tela3, text="Dimensões do produto:", font=("Arial", 10))
    label_dimensoes.pack(pady=5, padx=5)
    label_largura = tk.Label(tela3, text="Largura (cm):", font=("Arial", 10))
    label_largura.pack(pady=5, padx=5)
    entry_largura = tk.Entry(tela3, font=("Arial", 10))
    entry_largura.pack(pady=5, padx=5)
    label_altura = tk.Label(tela3, text="Altura (cm):", font=("Arial", 10))
    label_altura.pack(pady=5, padx=5)
    entry_altura = tk.Entry(tela3, font=("Arial", 10))
    entry_altura.pack(pady=5, padx=5)
    label_comprimento = tk.Label(tela3, text="Comprimento(cm):", font=("Arial", 10))
    label_comprimento.pack(pady=5, padx=5)
    entry_comprimento = tk.Entry(tela3, font=("Arial", 10))
    entry_comprimento.pack(pady=5, padx=5)
    label_peso = tk.Label(tela3, text="Peso (kg):", font=("Arial", 10))
    label_peso.pack(pady=5, padx=5)
    entry_peso = tk.Entry(tela3, font=("Arial", 10))
    entry_peso.pack(pady=5, padx=5)
    botao_buscar = tk.Button(tela3, text="Buscar", font=("Arial", 10), width=10, command=lambda: calcularfrete(entry_cep1.get(), entry_cep2.get(), entry_largura.get(), entry_altura.get(), entry_comprimento.get(), entry_peso.get()))
    botao_buscar.pack(pady=5, padx=5)
    botao_voltar = tk.Button(tela3, text="Voltar", font=("Arial", 10), width=10, command=lambda: (tela3.destroy(), tela2.deiconify()))
    botao_voltar.pack(pady=5, padx=5)
    textofrete = tk.Label(tela3, text='')
    textofrete.pack(pady=5, padx=5)
def opcao4tela():
    tela2.destroy()
    root.deiconify()

def abrir_tela2(nivel_acesso):
    root.withdraw()
    global tela2
    tela2 = tk.Toplevel(root)
    tela2.resizable(False, False)
    tela2.title("FRETINHO")
    tela2.geometry("600x400") 
    if nivel_acesso == 'admin':
        label = tk.Label(tela2, text="Bem-vindo, Administrador!", font=("Arial", 30))
    else:
        opcao1 = tk.Button(tela2, text="Buscar Endereço por CEP", font=("Arial", 10), width=30, command=lambda: opcao1tela())
        opcao1.pack(pady=5, padx=5)
        opcao2 = tk.Button(tela2, text="Buscar CEP por endereço", font=("Arial", 10), width=30, command=lambda: opcao2tela())
        opcao2.pack(pady=5, padx=5)
        opcao3 = tk.Button(tela2, text="Calcular Frete", font=("Arial", 10), width=30, command=lambda: opcao3tela())
        opcao3.pack(pady=5, padx=5)
        opcao4 = tk.Button(tela2, text="Sair", font=("Arial", 10), width=30, command=lambda: opcao4tela())
        opcao4.pack(pady=5, padx=5)
def adicionar_usuario(user, senha, email, nivel_acesso):
    if user not in usuarios and user != '' and senha != '' and email != '':
        usuarios[user] = {'senha': senha, 'nivel_acesso': nivel_acesso, 'email': email}
        with open('usuarios.txt', 'w') as usuarios_file:
            usuarios_file.write(str(usuarios))
        messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso')
    else:
        messagebox.showerror('Erro', 'Usuário já cadastrado')
def registrar():
    
    botao_login_admin.place(x=1000000)
    botao_login.place(x=1000000)
    botao_registro.place(x=1000000)
    entry_senha.place(x=1000000)
    label_senha.place(x=1000000)
    entry_usuario.place(x=1000000)
    label_usuario.place(x=1000000)



    def voltarparalogin():
        
        #removendo tela de cadastro
        email_entry.place(x=100000)
        email_label.place(x=100000)
        pass_entry.place(x=100000)
        pass_label.place(x=100000)
        user_label.place(x=100000)
        user_entry.place(x=100000)
        botao_voltar.place(x=100000)
        botao_adm.place(x=100000)
        botao_user.place(x=1000000)
        
        #voltando para tela inicial
        label_usuario.pack(pady=2)
        entry_usuario.pack(pady=1)
        label_senha.pack(pady=2)
        entry_senha.pack(pady=1)
        botao_login_admin.pack(pady=2)
        botao_login.pack(pady=2)
        botao_registro.pack(pady=2)

    botao_voltar = tk.Button(container_login, text="Voltar", command=voltarparalogin, font=("Arial", 7), width=6)
    botao_voltar.pack(pady=5) 
        
    
    
    #lista_email = []
    
    #tela de cadastro    
    email_label = tk.Label(container_login, text="Email:", font=("Arial", 11))
    email_label.pack(pady=2)
    
    email_entry = tk.Entry(container_login, font=("Arial", 11))
    email_entry.pack(pady=1)
    
    user_label = tk.Label(container_login, text="Usuário:", font=("Arial", 11))
    user_label.pack(pady=2)
    
    user_entry = tk.Entry(container_login, font=("Arial", 9))
    user_entry.pack(pady=1)                 
    
    pass_label = tk.Label(container_login, text="Senha:", font=("Arial", 11))
    pass_label.pack(pady=2)
    
    pass_entry = tk.Entry(container_login, font=("Arial", 9), show="*")
    pass_entry.pack(pady=1)
    
    botao_adm = tk.Button(container_login, text="Adm", font=("Arial", 9), width=10, command=lambda: adicionar_usuario(user_entry.get(), pass_entry.get(), email_entry.get(), 'admin'))
    botao_adm.pack(pady=2)
    
    botao_user = tk.Button(container_login, text="User", font=("Arial", 9), width=10, command=lambda: adicionar_usuario(user_entry.get(), pass_entry.get(), email_entry.get(), 'normal'))
    botao_user.pack(pady=2)

def obter_icone_da_web(url_icone):
    response = requests.get(url_icone)
    icone = Image.open(BytesIO(response.content))
    icone = ImageTk.PhotoImage(icone)
    return icone

# configuração da janela principal (utilizando tkinter, como a professora indicou)
root = tk.Tk()
root.resizable(False, False)
root.title("FRETINHO")
root.geometry("600x400")  # tamanho da root minimizada, ao iniciar.


url_icone = "https://i.pinimg.com/originals/dd/ac/b9/ddacb9b710c41b9d9bdba1547b449661.jpg"
icone = obter_icone_da_web(url_icone)
root.iconphoto(True, icone)

# imagem postada no pinterest para ser o background

url_imagem = "https://i.pinimg.com/originals/b8/4a/72/b84a72440b1053e7969371686353f046.png"
response = requests.get(url_imagem)
imagem_fundo = Image.open(BytesIO(response.content))
imagem_fundo = ImageTk.PhotoImage(imagem_fundo)

# código para colocar a imagem de fundo / background
fundo_label = tk.Label(root, image=imagem_fundo)
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)  # preenche toda a root

# frame para o container de login
container_login = tk.Frame(root, bg="white", width=300, height=200) 
container_login.place(relx=0.5, rely=0.5, anchor="center")

#entrada para o usuário
label_usuario = tk.Label(container_login, text="Usuário:", font=("Arial", 14), bg="white")
label_usuario.pack(pady=5) 

entry_usuario = tk.Entry(container_login, font=("Arial", 12)) 
entry_usuario.pack(pady=1)

# inserir para a senha
label_senha = tk.Label(container_login, text="Senha:", font=("Arial", 14), bg="white")
label_senha.pack(pady=5)

entry_senha = tk.Entry(container_login, show="*", font=("Arial", 12))
entry_senha.pack(pady=1)

# botão de login, juntamente a validação de dados com a função lá do começo do código
botao_login = tk.Button(container_login, text="Login", command=lambda: fazer_login('normal'), font=("Arial", 10), width=5) 
botao_login.pack(pady=5)

# botão de login para administrador
botao_login_admin = tk.Button(container_login, text="Admin - Login", command=lambda: fazer_login('admin'), font=("Arial", 10), width=10)
botao_login_admin.pack(pady=5)

#esquecendo a tela inicial mudando ela de posicao

    
botao_registro = tk.Button(container_login, text="Cadastre-se", command=registrar, font=('Arial', 10), width=10)
botao_registro.pack(pady=5)


root.mainloop()