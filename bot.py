import time
import telebot
from datetime import datetime, timedelta
import os


# Token do bot do Telegram
TOKEN = '7609406956:AAEKRxbV1_VRDhxOb2Lc342P3ma9VRivDN8'
chat_id = '-4637658746'  # Chat ID do seu grupo no Telegram

# Função para enviar a mensagem para o Telegram
def msgtelegram(nome, entrada, saida):
    bot = telebot.TeleBot(TOKEN)
    mensagem = f"""
___________________________________
    🧑‍💼{nome}, Bom almoço!
___________________________________\n
🍽️Horário de entrada: {entrada}🗓️\n
‼️Seu almoço terminará: {saida}
Irei te avisar 5 minutos antes de terminar!\n"""
    bot.send_message(chat_id, mensagem)
    
# Limpa a tela do terminal e manda não fechar o programa
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[33m-------------------- ALMOÇO ------------------\n\033[0m")
    print(f"\033[31m---------- NÃO FECHE O PROGRAMA !!! ----------\n\n\033[0m")
    print(f"\033[34mBom almoço, {nome}! Seu almoço terminará em 1 Hora.\033[0m\n")
    print(f"\033[32mHorário de entrada: {entrada}\033[0m")
    print(f"\033[31mHorário de saída: {saida}\033[0m\n")

    time.sleep(5)  # Espera 55 minutos (3300 segundos)

    mensagem = f"""\n
___________________________________
‼️ {nome}, seu almoço terminou! ‼️
___________________________________\n
✍️Horário de saída: {saida}🗓️
💼Agora você pode voltar ao trabalho!"""
    bot.send_message(chat_id, mensagem)

# Função para perguntar o nome e se bateu o ponto
def infos():
    while True:
        nome = input("Digite seu nome: ").strip().title()
        ponto = input("Você já bateu o ponto? (sim/não): ").lower()
        
        if ponto in ['sim', 's', '']:
            print(f"Ótimo, {nome}! Você já bateu o ponto.")
            entrada = datetime.now().strftime('%H:%M')
            print(f"Você entrou às {entrada}. O horário de almoço será marcado daqui a 50 minutos!")
            saida = (datetime.now() + timedelta(minutes=60)).strftime('%H:%M')
            msgtelegram(nome, entrada, saida)
            break

        elif ponto in ['não', 'n']:
            print(f"{nome}, assim que você bater o ponto, me avise!\n")      
        
# Rodando a coleta de informações
infos()
