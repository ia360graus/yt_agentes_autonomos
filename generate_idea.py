import csv
import json
import openai

openai.api_key = ''

def ler_csv(arquivo):
    videos = []
    with open(arquivo, mode='r', encoding='utf-8') as file:
        leitor = csv.DictReader(file)
        for linha in leitor:
            titulo = linha['Título do vídeo']
            likes = linha['Quantidade de Likes']
            visualizacoes = linha['Quantidade de Visualizações']
            data_publicacao = linha['Data de publicação do vídeo']
            videos.append({"título do video": titulo, "likes": likes, 
            "visualizacoes": visualizacoes, "data_publicacao": data_publicacao})
    return json.dumps(videos, ensure_ascii=False)



def enviar_para_api(pergunta):
    resposta = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      max_tokens=1000,
      messages=[
            {"role": "user", "content": pergunta},
      ]
    )
    return resposta.choices[0].message['content']

yt_dados = ler_csv('videos.csv')

pg1 = f"""Com base nos dados coletados de canais de youtube de ciência e tecnologia.
Retire vídeos com temas inadequados, mantenha apenas vídeos relacionados a ciência e tecnologia.

Identifique os 5 vídeos mais populares com base na relação entre visualizações e likes.
Responda na seguinte estrutura:

TOP 5 Vídeos:

Título do Vídeo:
Quantidade de Likes:
Quantidade de Visualizações:
Relação entre Visualizações e Likes:

Não escreva nada além da estrutura mencionada acima.

Dados do Youtube:
{yt_dados}
"""

top_5_videos = enviar_para_api(pergunta=pg1)

pg2 = f"""Com base nos 5 vídeos mais populares sobre ciência e tecnologia, 
identifique trending topics e me de 3 ideias para conteúdo para o youtube 
fora da caixa e que possam gerar muito engajamento.

Escreva as ideias utilizando exatamente essa estrutura:

Ideias:

1 - Aqui Você coloca a ideia 1.

2 - Aqui Você coloca a ideia 2.

e assim por diante.

Dados dos Vídeos:
{top_5_videos}"""

ideias = enviar_para_api(pergunta=pg2)

# Vamos pegar somente a parte após "Ideias:"
parte_ideias = ideias.split("Ideias:")[1].strip()

# Imprimimos as ideias na tela
print("Ideias:\n" + parte_ideias)

# Vamos agora escrever as ideias em um arquivo de texto
nome_arquivo = 'ideias.txt'
with open(nome_arquivo, 'w') as arquivo:
    arquivo.write("Ideias:\n" + parte_ideias)

print(f"\nAs ideias foram salvas no arquivo {nome_arquivo}!")