import csv
import json
import openai
from colorama import Fore

openai.api_key = ''


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    return conteudo


def enviar_para_api(personality, user_prompt, conversa):

    conversa.insert(0, {"role": "system", "content": personality})
    conversa.append({"role": "user", "content": user_prompt})

    resposta = openai.ChatCompletion.create(
      model="gpt-4",
      max_tokens=2000,
      messages=conversa
    )
    
    resposta = resposta.choices[0].message['content']


    conversa.append({"role": "assistant", "content": f"{resposta}"})

    return resposta



ideias = ler_arquivo('ideias.txt')
joao_system_prompt = ler_arquivo('system_prompt_joao.txt')
joao_system_prompt = joao_system_prompt + f'\n {ideias}'

jose_system_prompt = ler_arquivo('system_prompt_jose.txt')

conversa_joao = []
conversa_jose = []

user_message = 'Olá João, aqui é o José, estou pronto para ouvir suas ideias.'


print(Fore.BLUE,f'José: {user_message}\n\n')

while True:

    user_message = enviar_para_api(personality=joao_system_prompt, user_prompt=user_message, conversa=conversa_joao)

    print(Fore.GREEN,f'João: {user_message}\n\n')

    if 'Ideia Final Escolhida' in user_message:
        break

    user_message = enviar_para_api(personality=jose_system_prompt, user_prompt=user_message, conversa=conversa_jose)

    print(Fore.BLUE,f'José: {user_message}\n\n')

