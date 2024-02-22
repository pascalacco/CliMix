from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from .llm_utils import prompt_gpt,prompt_gpt_bis
import random
from archiveur import DataManager
from constantes import *
import numpy.random as rd

def generate_prompts(group,team):
    load_dotenv()  

    var = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=var)
    dm=DataManager(group,team)
    roles=dm.get_roles()
    shuffled_roles = {k: roles[k] for k in random.sample(roles.keys(), len(roles))}
    i=0
    for r in shuffled_roles.values():
        #déterminons s'il va s'agir d'un entretien ou d'un reportage
        rdm=rd.rand(1)
        if rdm>0.5:
            type="entretien"
        else:
            type="reportage"
        #prompt=prompt_gpt(r,dm)
        prompt=prompt_gpt_bis(r,dm)
        print(prompt+"Écrire un article journalistique de 200 mots sous la forme d'un {}".format(type))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            #model="gpt-3.5",
            messages=[
            #{"role": "system", "content": "On va de produire des articles pour une page de journal. On va simuler un reportage ou une interview pour chaque personnage de notre jeu."},
            {"role": "system", "content": "Écrire un article journalistique de 200 mots sous la forme d'un {}. Produire un article vraisemblable sans éléments étranges. Le genre que tu attribueras au sujet sera basé sur son nom et non sur le genre que tu déduis du prompt.".format(type)},
            {"role":"user","content":"Écrire un article journalistique de 200 mots sous la forme d'un {}".format(type)+prompt}
            ]
        )
        output=str(completion.choices[0].message.content)
        dm.update_gpt_text(character_number=i,text=output)
        i+=1
        if i == 3:
            break

    