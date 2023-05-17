
import mysql.connector; import os.path; import re, uuid ;import socket; import platform;
import psutil; from datetime import datetime; from mysql.connector import Error; from time import sleep;
import ipaddress; import sys; import winreg;




'''
Obter informações do computador:
'''
windows_linux = platform.system()
mac_atual_usado = '-'.join(re.findall('..', '%012x' % uuid.getnode()))

def get_mac_txt():
    mac_andress = '-'.join(re.findall('..', '%012x' % uuid.getnode()))
    mac_file = 'mac.txt'
    
    if os.path.isfile(mac_file):    
        with open(mac_file, 'r') as f:
            mactxt = f.read()
    else:
        mactxt = mac_andress
        with open(mac_file, 'w') as f: # Salvar o valor do MAC address em um arquivo
            f.write(mactxt)
    return mactxt

def get_memory():
    memoria_decimal = psutil.virtual_memory().total / (1024.0 **3)
    memoria_arredondanda = round(memoria_decimal,3)
    return memoria_arredondanda

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def verificar_mac():
    if mac_atual_usado == get_mac_txt():
        mac_iguais = True
    else:
        mac_iguais =False
    return mac_iguais

if windows_linux == 'Windows':
    def get_windows_edition():
        reg_path = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                product_name = winreg.QueryValueEx(key, 'ProductName')[0]
                if sys.getwindowsversion().major == 10:
                    if 'Professional' in product_name:
                        return 'Windows 10 Professional'
                    elif 'Enterprise' in product_name:
                        return 'Windows 10 Enterprise'
                    elif 'Education' in product_name:
                        return 'Windows 10 Education'
                    else:
                        return 'Windows 10 Home'
                elif sys.getwindowsversion().major == 6 and sys.getwindowsversion().minor == 1:
                    edition_id = winreg.QueryValueEx(key, 'EditionID')[0]
                    if edition_id == 'Professional':
                        return 'Windows 7 Professional'
                    elif edition_id == 'HomeBasic':
                        return 'Windows 7 Home Basic'
                    elif edition_id == 'HomePremium':
                        return 'Windows 7 Home Premium'
                    elif edition_id == 'Starter':
                        return 'Windows 7 Starter'
                    elif edition_id == 'Ultimate':
                        return 'Windows 7 Ultimate'
                    else:
                        return 'Windows 7'
                else:
                    return 'Windows'
        except:
            return 'Unknown'


    def get_processador():
        os.system('wmic cpu get name>processador.txt.')

        with open("processador.txt", "r") as arquivo:
            processador = arquivo.read()

            processador = processador.split()
            
            result = [string.replace('\x00', '') for string in processador]
            
        
            result = list(filter(None,result))  
            for item in result:
                if item == 'CPU':
                    result.remove('CPU')
            for item in result:
                if item == '@':
                    result.remove('@')

            del result [0:2]
            
            result = [' '.join(result)]
            processador_name = result[0]
        return processador_name
    
    processador_name = get_processador()
    edicao_windows = get_windows_edition()
else: 
    processador_name = 'Unknown'
    edicao_windows = 'Unknown'


Terminal = socket.gethostname()
ip_local = extract_ip()
mac_txt = get_mac_txt()
versionwindows = platform.version()
memoria = get_memory()
data = datetime.today().strftime('%Y-%m-%d') 





'''
Verificação de qual loja o computador deve ser:
'''

def numero_da_loja_ip():

    Num_loja = ip_local[8:]
    Lista_do_numero_da_loja = []
    
    for i in Num_loja:
        if i == '.':
            break
        else:
            Lista_do_numero_da_loja.append(i)
    Num_loja = [''.join(Lista_do_numero_da_loja)]
    
    return Num_loja[0]

def numero_loja_terminal():

    Terminal_minusculo = Terminal.lower()
    
    if Terminal_minusculo[0:8] == 'terminal':
        num_term = Terminal_minusculo[8:10]
    
    elif Terminal_minusculo[0:8] == 'consulta':
        num_term = Terminal_minusculo[8:10]
    
    elif Terminal_minusculo[0:8] == 'servidor':
       num_term = Terminal_minusculo[8:10]
   
    elif Terminal_minusculo[0:8] == 'terposto':
        num_term = 'posto' + Terminal_minusculo[8:10]
    
    elif Terminal_minusculo[0:2].isnumeric() or Terminal_minusculo[0:3].isnumeric():
        if Terminal_minusculo[0:2].isnumeric():numero = Terminal_minusculo[0:2] 
        if Terminal_minusculo[0:3].isnumeric():numero = Terminal_minusculo[0:3]
        num_term = 'posto' + numero 

    else:
        num_term = 'desconhecido'
    
    if num_term[0:2] == '00': num_term = 'matriz'
    elif num_term[0] == '0': num_term = num_term[1]
    
    return num_term

                
num_ip = numero_da_loja_ip()
num_term = numero_loja_terminal()

if num_term == 'matriz' and num_ip == '1': loja = num_term 

elif num_term == num_ip: loja = num_ip

elif num_term[0:6] == 'posto': loja = num_term #loja recebe o nome posto + loja do posto
    
elif num_term != num_ip and num_term != 'desconhecido': loja = num_term # se o nome do computador for terminal, servidor ou consulta, porem o ip estive fora da faixa da loja, ele considera a loja do nome do pc
    
else: loja = 'desconhecido' #se tiver nome aleatorio ele recebe loja desconhecida, mesmo tendo a faixa de ip correta


'''
fazendo conexão com mysql:
'''
try:
    conexao = mysql.connector.connect(
        host = '',
        user = '',
        password = '',
        database = '',
        auth_plugin='mysql_native_password')
    cursor = conexao.cursor()  
    
    '''
    Funções para CRUD no banco:
    '''
    
    def selecionar_itens_bd(comando):
        cursor.execute(comando)
        resultado = cursor.fetchall()
        conexao.commit()
    
        return resultado

    def modificar_itens_bd(comando):
        cursor.execute(comando)
        conexao.commit()
        
    '''
    Executando comandos para o banco MYSQL:
    '''
    info_computador_bd = selecionar_itens_bd('SELECT mac FROM computadores WHERE mac = "{0}"'.format(mac_txt)) 
    info_date_computer = selecionar_itens_bd('SELECT Create_Date FROM computadores WHERE mac = "{0}"'.format(mac_txt))

    if windows_linux == 'Windows':
        if info_computador_bd == []:
            modificar_itens_bd('INSERT INTO computadores (mac, terminal, ip, processador, memoria, windows_linux, edicao, versao_sistema,loja, Create_Date)\
            VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}");'.format(mac_txt,Terminal,ip_local,processador_name,memoria,windows_linux, edicao_windows, versionwindows,loja,data))
            
        elif info_computador_bd[0][0] == mac_txt:
            modificar_itens_bd('UPDATE computadores SET terminal="{0}", ip="{1}", processador="{2}", memoria="{3}", windows_linux="{4}", edicao = "{5}",\
            versao_sistema="{6}", loja = "{7}", Update_Date ="{8}" WHERE mac="{9}"'.format(Terminal,ip_local,processador_name,memoria,windows_linux,edicao_windows, versionwindows,loja,data,mac_txt))
   

    if windows_linux == 'Windows' and verificar_mac() == False:
        mac_antigo = mac_txt
        mac_novo = mac_atual_usado
        
        get_bd_mac_antigo = selecionar_itens_bd('SELECT mac_antigo FROM mac_alterado WHERE mac_antigo = "{0}"'.format(mac_antigo))

        if get_bd_mac_antigo == []:
            modificar_itens_bd('INSERT INTO mac_alterado (mac_antigo,mac_novo,Update_Date,terminal_mac) VALUES ("{0}","{1}","{2}","{3}")'.format(mac_antigo,mac_novo,data,Terminal))
        else: 
            modificar_itens_bd('UPDATE mac_alterado SET mac_novo="{0}", Update_Date="{1}", terminal_mac="{2}" WHERE mac_antigo="{3}"'.format(mac_novo,data,Terminal, mac_antigo))


except Error as erro: 
    print("Falha ao inserir dados no mysql: {}".format(erro))
    print("Entre em contato com a Informatica do Feirao dos Moveis")
    sleep(30)

finally:
    if(conexao.is_connected()):

        cursor.close()
        conexao.close()
        





