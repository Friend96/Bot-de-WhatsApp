from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import tkinter as tk
import re
from PIL import Image, ImageTk


def iniciar_bot():
    servico = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=servico, options=options)
    
    driver.get('https://web.whatsapp.com')

    # esperar ate escanear o QR code
    input("Pressione Enter após escanear o QR code:")

    # variavel global
    global_var = False
    

    def buscar_grupo(grupo):
        global global_var
        global_var = True

        is_minimized = driver.execute_script("return document.hidden")
        if is_minimized:
            try:
                driver.maximize_window()
                driver.set_window_size(1024, 768)
            except:
                pass
        else:
            pass
        try:
            driver.refresh()
            time.sleep(10)
            driver.find_element('xpath', '//*[@id="side"]/div[2]/button[1]').click()
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(grupo)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            pass

    def ver_grupos():
        def remove_emojis(text):
            emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"       
            u"\U0001F300-\U0001F5FF" 
            u"\U0001F680-\U0001F6FF" 
            u"\U0001F1E0-\U0001F1FF"             
            u"\U00002500-\U00002BEF"  
            u"\U00002702-\U000027B0"  
            u"\U00002702-\U000027B0"  
            u"\U000024C2-\U0001F251"  
            u"\U0001f926-\U0001f937"    
            u"\U00010000-\U0010ffff"  
            u"\u2640-\u2642"           
            u"\u2600-\u2B55"           
            u"\u200d"                  
            u"\u23cf"                  
            u"\u23e9"                  
            u"\u231a"                  
            u"\ufe0f"                  
            u"\u3030"                  
            "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        driver.maximize_window()
        driver.set_window_size(1024, 768)
        driver.find_element(By.XPATH, '//*[@id="side"]/div[2]/button[3]').click()
        time.sleep(4)

        ultimo_tamanho = 0
        group_names = set()
        
        is_minimized = driver.execute_script("return document.hidden")
        if is_minimized:
            try:
                driver.maximize_window()
                driver.set_window_size(1024, 768)
            except:
                pass
        else:
            pass
        tentativas_sem_novos_itens = 0
        while tentativas_sem_novos_itens < 5:
            groups = driver.find_elements(By.XPATH, '//span[@class="x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e"]')
            new_group_names = [remove_emojis(group.get_attribute("title")) for group in groups]
            group_names.update(new_group_names)
            is_minimized = driver.execute_script("return document.hidden")
            if is_minimized:
                try:
                    driver.maximize_window()
                    driver.set_window_size(1024, 768)
                except:
                    pass
            else:
                pass
            tamanho_atual = len(group_names)
            if tamanho_atual == ultimo_tamanho:
                tentativas_sem_novos_itens += 1
            else:
                tentativas_sem_novos_itens = 0
                ultimo_tamanho = tamanho_atual
            is_minimized = driver.execute_script("return document.hidden")
            if is_minimized:
                try:
                    driver.maximize_window()
                    driver.set_window_size(1024, 768)
                except:
                    pass
            else:
                pass
            pane_side = driver.find_element(By.XPATH, '//*[@id="pane-side"]')
            driver.execute_script("arguments[0].scrollBy(0, 300);", pane_side)
            time.sleep(2)
            
            print("\033[1;32m Procurando grupos. . . \033[m")

            is_minimized = driver.execute_script("return document.hidden")
            if is_minimized:
                try:
                    driver.maximize_window()
                    driver.set_window_size(1024, 768)
                except:
                    pass
            else:
                pass
        driver.refresh()
        time.sleep(10)
        return group_names

    def pegar_membros(grupo):
        is_minimized = driver.execute_script("return document.hidden")
        if is_minimized:
            try:
                driver.maximize_window()
                driver.set_window_size(1024, 768)
            except:
                pass
        else:
            pass
        try:
            membros = []
            menu_grupo = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[1]')
            menu_grupo.click()
            time.sleep(2)
            
            # Abre a lista de participantes
            xpaths = [
                '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[6]/div[1]/div/div[1]',
                '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[1]/div/div[1]'
            ]
            for xpath in xpaths:
                try:
                    participantes = driver.find_element(By.XPATH, f"{xpath}//span[contains(text(), 'Membros:')]")
                    participantes.click()
                    time.sleep(2)
                except:
                    continue
            # pega os membros
            n = 1
            while True:
                membros_elementos = driver.find_elements(By.XPATH, f'//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[{n}]')

                for elemento in membros_elementos:
                    membros.append(elemento.text)

                if len(membros_elementos) == 0:
                    break
                n += 1 

            return membros
        except:
            def buscar_novamente():
                def remove_emojis(text):
                    emoji_pattern = re.compile(
                    "["
                    u"\U0001F600-\U0001F64F"       
                    u"\U0001F300-\U0001F5FF" 
                    u"\U0001F680-\U0001F6FF" 
                    u"\U0001F1E0-\U0001F1FF"             
                    u"\U00002500-\U00002BEF"  
                    u"\U00002702-\U000027B0"  
                    u"\U00002702-\U000027B0"  
                    u"\U000024C2-\U0001F251"  
                    u"\U0001f926-\U0001f937"    
                    u"\U00010000-\U0010ffff"  
                    u"\u2640-\u2642"           
                    u"\u2600-\u2B55"           
                    u"\u200d"                  
                    u"\u23cf"                  
                    u"\u23e9"                  
                    u"\u231a"                  
                    u"\ufe0f"                  
                    u"\u3030"                  
                    "]+", flags=re.UNICODE)
                    return emoji_pattern.sub(r'', text)
                
                driver.maximize_window()
                driver.set_window_size(1024, 768)
                driver.refresh()
                time.sleep(10)
                driver.find_element(By.XPATH, '//*[@id="side"]/div[2]/button[3]').click()
                time.sleep(4)

                ultimo_tamanho = 0
                group_names = set()
                
                is_minimized = driver.execute_script("return document.hidden")
                if is_minimized:
                    try:
                        driver.maximize_window()
                        driver.set_window_size(1024, 768)
                    except:
                        pass
                else:
                    pass
                tentativas_sem_novos_itens = 0
                while tentativas_sem_novos_itens < 5:
                    groups = driver.find_elements(By.XPATH, '//span[@class="x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e"]')
                    new_group_names = [remove_emojis(group.get_attribute("title")) for group in groups]
                    group_names.update(new_group_names)
                    is_minimized = driver.execute_script("return document.hidden")
                    if is_minimized:
                        try:
                            driver.maximize_window()
                            driver.set_window_size(1024, 768)
                        except:
                            pass
                    else:
                        pass
                    
                    for grupo_escolhido in groups:
                        if remove_emojis(grupo_escolhido.get_attribute("title")) == grupo:
                            grupo_escolhido.click()
                            break

                    tamanho_atual = len(group_names)
                    if tamanho_atual == ultimo_tamanho:
                        tentativas_sem_novos_itens += 1
                    else:
                        tentativas_sem_novos_itens = 0
                        ultimo_tamanho = tamanho_atual
                    
                    is_minimized = driver.execute_script("return document.hidden")
                    if is_minimized:
                        try:
                            driver.maximize_window()
                            driver.set_window_size(1024, 768)
                        except:
                            pass
                    else:
                        pass
                    pane_side = driver.find_element(By.XPATH, '//*[@id="pane-side"]')
                    driver.execute_script("arguments[0].scrollBy(0, 300);", pane_side)
                    time.sleep(2)

                    is_minimized = driver.execute_script("return document.hidden")
                    if is_minimized:
                        try:
                            driver.maximize_window()
                            driver.set_window_size(1024, 768)
                        except:
                            pass
                    else:
                        pass

            global global_var

            if global_var == True:
                global_var = False
                buscar_novamente()
                return pegar_membros(grupo)
            else:
                print()
                print("\033[1;31m Grupo não encontrado \033[m")
                print()

    def adicionar_ao_grupo(membros, grupo_destino):
        is_minimized = driver.execute_script("return document.hidden")
        if is_minimized:
            try:
                driver.maximize_window()
                driver.set_window_size(1024, 768)
            except:
                pass
        else:
            pass
        try:
            buscar_grupo(grupo_destino)
            menu_grupo = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[1]')
            menu_grupo.click()
            time.sleep(2)
            xpaths = [
                '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]/div[1]/div/div/span',
                '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[6]/div[2]/div[1]/div[1]/div/div/span'
            ]
            for xpath in xpaths:
                try:
                    driver.find_element('xpath', xpath).click()

                    input_element = driver.find_element('xpath', '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div')
                    time.sleep(2)
                    for membro in membros:
                        input_element.clear()
                        input_element.send_keys(membro)
                        time.sleep(2)
                        input_element.send_keys(Keys.ENTER)
                        time.sleep(1)
                except:
                    continue
            driver.find_element('xpath', '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span[2]/div/div/div').click()
            time.sleep(1)
            driver.find_element('xpath', '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]').click()
            time.sleep(4)
            driver.quit()
        except:
            print("\033[1;31mNinguem foi adicionado.\033[m")
            driver.quit()

    nomes_grupo = ver_grupos()

    numeros = []
    for nome_grupo in nomes_grupo:
        if nome_grupo == "None":
            continue
        if nome_grupo.strip() == "":
            continue
        print()
        while True:
            deseja = input(f'Quer adicionar alguem do grupo \033[1;33m{nome_grupo}\033[m?[s/n] ')
            if deseja in ['n', 's']:
                break
            else:
                print("\033[1;31m Entrada inválida. Por favor, digite apenas 'n' ou 's'.\033[m")
        print()
        if deseja == "n":
            continue
        try:
            buscar_grupo(nome_grupo)
            membros = pegar_membros(nome_grupo)
            for membro in membros:
                print("=-"*60)
                print("\033[1;33m", nome_grupo, "\033[m")
                print("\033[1;36m")
                print(membro)
                print("\033[m")
                while True:
                    res = input("Deseja adicionar ao grupo?[s/n] ")
                    if deseja in ['n', 's']:
                        break
                    else:
                        print("\033[1;31m Entrada inválida. Por favor, digite apenas 'n' ou 's'.\033[m")
                if res == "s":
                    def extrair_numeros_lista(membro):
                        def extrair_numeros(texto):
                            padrao = r'\+?\d{1,3} \d{1,3} \d{3,5}[- ]?\d{4,5}'
                            return re.findall(padrao, texto)
                        
                        numeros = extrair_numeros(membro)
                        return numeros
                    numeros.extend(extrair_numeros_lista(membro))
        except:
            continue
    print()
    add_grupo = input("Escreva o nome do grupo que você quer adicionar os membros: ")
    adicionar_ao_grupo(numeros, add_grupo)
    print("terminou")
    time.sleep(20)
    
    # Fechar navegador
    driver.quit()

janela = tk.Tk()
janela.title("Bot WhatsApp")

janela.geometry("400x300")

# Cria botão
botao = tk.Button(janela, text="Iniciar Bot_whatsapp", command=iniciar_bot, width=20, height=3, bg='green', fg='white')
botao.pack(pady=20)

janela.mainloop()