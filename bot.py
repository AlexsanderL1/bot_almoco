import time
import telebot
from datetime import datetime, timedelta
import threading
import os

# Token do seu bot
TOKEN = '7609406956:AAEKRxbV1_VRDhxOb2Lc342P3ma9VRivDN8'
bot = telebot.TeleBot(TOKEN)

# ID do grupo onde o bot vai mandar mensagens
chat_id = '-4637658746'

# Seu ID pessoal (trocar depois se necessário)
SEU_ID = 5988594763  # <-- já coloquei o seu aqui!

user_state = {}

# Função de envio com delay
def agendar_mensagem(chat_id, nome, saida):
    time.sleep(55 * 60)  # Espera 55 minutos
    mensagem = f"""
___________________________________
‼️ {nome}, seu almoço terminará em 5 minutos! ‼️
___________________________________

✍️Horário de saída: {saida}🗓️
💼Prepare-se para voltar ao trabalho!
"""
    bot.send_message(chat_id, mensagem)

# Comando para descobrir seu próprio ID
@bot.message_handler(commands=['id'])
def enviar_id(message):
    bot.send_message(message.chat.id, f"Seu ID é: {message.from_user.id}")

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
            threading.Thread(target=agendar_mensagem, args=(chat_id, nome, saida)).start()

            # Remove o estado do usuário
            del user_state[user_id]
        else:
            bot.send_message(message.chat.id, "Tudo bem! Me avise quando bater o ponto com /almoco.")
            del user_state[user_id]

# Comando para finalizar o bot
@bot.message_handler(commands=['fim'])
def fim(mensagem):
    if mensagem.from_user.id == SEU_ID:
        bot.send_message(mensagem.chat.id, "Encerrando o bot...")
        os._exit(0)  # Força o encerramento
    else:
        bot.send_message(mensagem.chat.id, "Você não tem permissão para isso.")

# Inicia o bot
print("Bot rodando...")
bot.remove_webhook()
bot.infinity_polling()
