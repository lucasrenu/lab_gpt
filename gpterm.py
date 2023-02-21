import os
import cv2
import sys
import shutil
import openai
import requests
from dotenv import load_dotenv
from random import randint

load_dotenv()

openai.api_key = os.getenv('API_KEY')

def gpt_chat(prompt):
    
    response = openai.Completion.create(
		engine = "text-davinci-003",
		prompt = prompt,
		temperature = 0.7,
		max_tokens = 1000,
	)
    
    return response.choices[0].text

def gpt_image(prompt):
    response = openai.Image.create(prompt = prompt, n = 1, size = "1024x1024")
    return requests.get(response['data'][0]['url'], stream = True)

if __name__ == '__main__':
    prompt = ' '.join(sys.argv[1:])
    if '-' == sys.argv[1][0]:
        prompt = prompt[3:]
        match(sys.argv[1]):
            case '-i':
                name = f'img{randint(1,100)}.png'
                with open(name, 'wb') as out_file:
                    shutil.copyfileobj(gpt_image(prompt).raw, out_file)
                    
                imagem = cv2.imread(name)
                cv2.imshow("Original", imagem)
            case '-h':
                print("""
                    gpterm\033[1m -<opção>\033[m <descrição>
                    gpterm\033[1m -i\033[m ... -> Gerar imagem com base na descrição
                    gpterm ... -> Pesquisar                                       
                    gpterm\033[1m -h\033[m -> Ajuda
                """)
            case _:
                print('Opção inválida!')
    else:
    	print(gpt_chat(prompt))