import time
import telebot
from datetime import datetime, timedelta
import threading

# Token do seu bot
TOKEN = '7609406956:AAEKRxbV1_VRDhxOb2Lc342P3ma9VRivDN8'
bot = telebot.TeleBot(TOKEN)
chat_id = '-4637658746'

# Dicionário para armazenar estados de cada usuário
user_state = {}

# Função de envio com delay
def agendar_mensagem(nome, saida):
    time.sleep(10)  # Espera 55 minutos
    mensagem = f"""
___________________________________
‼️ {nome}, seu almoço terminou! ‼️
___________________________________

✍️Horário de saída: {saida}🗓️
💼Agora você pode voltar ao trabalho!
"""
    bot.send_message(chat_id, mensagem)

# Início do processo com o comando /almoco
@bot.message_handler(commands=['almoco'])
def iniciar_almoco(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Como posso te chamar?")
    user_state[user_id] = {'step': 'nome'}

# Captura e gerencia as mensagens dos usuários
@bot.message_handler(func=lambda message: True)
def responder_mensagens(message):
    user_id = message.from_user.id

    # Ignora se o usuário não iniciou com /almoco
    if user_id not in user_state:
        return

    state = user_state[user_id]

    # Etapa 1: nome
    if state['step'] == 'nome':
        state['nome'] = message.text.strip().title()
        state['step'] = 'ponto'
        bot.send_message(message.chat.id, f"{state['nome']}, você já bateu o ponto? (sim/não)")
        return

    # Etapa 2: ponto
    elif state['step'] == 'ponto':
        if message.text.lower() in ['sim', 's', '']:
            nome = state['nome']
            entrada = datetime.now().strftime('%H:%M')
            saida = (datetime.now() + timedelta(minutes=60)).strftime('%H:%M')

            mensagem = f"""
___________________________________
    🧑‍💼{nome}, Bom almoço!
___________________________________

🍽️Horário de entrada: {entrada}🗓️
‼️Seu almoço terminará: {saida}
Irei te avisar 5 minutos antes de terminar!
"""
            bot.send_message(chat_id, mensagem)

            # Iniciar o timer para envio automático depois
            threading.Thread(target=agendar_mensagem, args=(nome, saida)).start()

            # Remove o estado do usuário
            del user_state[user_id]
        else:
            bot.send_message(message.chat.id, "Tudo bem! Me avise quando bater o ponto com /almoco.")
            del user_state[user_id]

# Inicia o bot
print("Bot rodando...")
bot.infinity_polling()
