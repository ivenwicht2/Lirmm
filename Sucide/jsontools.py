import json
import os
import numpy as np
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source,render
import matplotlib.pyplot as plt

def _map_section(data,typeQ) :
    for i in range(len(data['quests'])):
        if data['quests'][i]['type'] == typeQ :
            return i
    return -1


def _construct(data,question,parent,user='',questionnaire_type = 'None',ordre=-1):
    """
    Input data (dictionnaire), le nouvelle utilisateur. Question (dictionnaire) ,le total.
         String qui represente le parent (path). String qui represente l'utilisateur actuelle (nom du json)

    Output :  Dictionnaire 

    Fonction :  Ajouter les questions du nouvelle utilisateur dans 
                un autre dictionnaire ( le dictionnaire qui regroupe toutes les questions)
 
    """

    if parent == ['root']:
        num = _map_section(data,questionnaire_type)
        if num == -1 : return question 
        root =  data['quests'][num]["dataquestionnaire"]
    else :
        root = data


    if user == '':
        try :
            user = data['logs'][0]['IDuser']

        except :
            if "unknow" not in question :
                user = "unknow"
            else :
                user = 'unknow'
                i = 0
                while user in question :
                    i+=1
                    user = 'unknow{}'.format(i) 
        question[user] = {}


    for element in root:
        typeQ = element['answerType']

        if typeQ not in question[user] :
            question[user][typeQ] = {}

        question[user][typeQ][element['code']] = {}

        ordre += 1

        if typeQ == "Range":
            if 'required' in element : 
                required = 'true'
            else : 
                required = 'false' 
            if 'sousquest' in element['options'] :
                question[user][typeQ][element['code']] = {
                    'value' : element['value'],
                    'subtitle':element['subtitle'],
                    'subquestions':{},
                    'answered':element['answered'],
                    'root' : parent,
                    'required':required,
                    'ordre':ordre}  

                parent.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    _construct([subquestion],question,parent,user,ordre)

            else :
                question[user][typeQ][element['code']] = {
                    'value' : element['value'],
                    'answered':element['answered'],
                    'min-max' : [element['options']['min'] ,element['options']['max']],
                    'root':parent,
                    'required':required,
                    'ordre':ordre}
            


        if typeQ == "Radio" :
            parent.append(element['code'])
            for subquestion in element['questionOptions']:
                if 'required' in subquestion : 
                    required = 'true'
                else :
                     required = 'false'
                question[user][typeQ][element['code']][subquestion['text']] = { 
                    "checked": subquestion['checked'] ,
                    'answered':element['answered'],
                    "value": subquestion['value'],
                    "root": parent,
                    'required':required,
                    'ordre':ordre}

                ordre += 1


        if typeQ == 'Checkbox' :
            parent.append(element['code'])
            for subquestion in element['questionOptions'] :
                if 'required' in subquestion  : 
                    required = 'true'
                else :
                    required = 'false'
                question[user][typeQ][element['code']][subquestion['text']] = { 
                    "checked": subquestion['checked'] ,
                    'answered':element['answered'],
                    "value": subquestion['value'],
                    "root": parent,
                    'required':required,
                    'ordre':ordre}
                ordre += 1
      
        if typeQ == 'Text' :
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            question[user][typeQ][element['code']] = {
                'value' : element["value"],
                'answered':element['answered'],
                'root' : parent,
                'required':required,
                'ordre':ordre
                }

        if typeQ == 'YesNo':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            if 'sousquest' in element['options'] :
                question[user][typeQ][element['code']] = {
                    'value' : element['checked'],
                    'answered':element['answered'],
                    'subquestion_name' : {element['options']['sousquest'][0]['code']},
                    'subquestions':{},
                    'subtitle' :element['options']['sousquest'][0]['subtitle'],
                    'root' : parent,
                    'required':required,
                    'ordre':ordre}
                
                parent.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    _construct([subquestion],question,parent,user,ordre)

            else :
                question[user][typeQ][element['code']] = {
                    'value' : element['checked'],
                    'answered':element['answered'],
                    'root' : parent,
                    'required':required,
                    'ordre':ordre }


        if typeQ == 'Contact':
            if 'required' in element: 
                required = 'true'
            else :
                required = 'false'

            question[user][typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : parent,
                'required':required,
                'ordre':ordre}

                
        if typeQ == 'Time':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            question[user][typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : parent,
                'required':required,
                'ordre':ordre }

        if typeQ == 'Input':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            question[user][typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : parent,
                'required':required,
                'ordre':ordre }


        if typeQ == 'Section':
            if 'required' in element: 
                required = 'true'
            else :
                required = 'false'
            if 'sousquest' in element['options'] :
                question[user][typeQ][element['code']] = {
                    'subtitle' :element['subtitle'],
                    'answered':element['answered'],
                    'root' : parent,
                    'required':required,
                    'ordre':ordre }

                parent.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    _construct([subquestion],question,parent,user,ordre)
        parent = ['root']

    return question



def import_json(source,questionnaire_type):
    """
    Input : PATH du dossier source 

    Output : Dictionnaire  dans le format suivant
            
            User1:
                    Type_de_question_1 :
                                        question1
                                        question2
                                        ....
                    Type_de_question_2 :
                                        question1
                                        question2
                                        ....
                    .....
            user2:
            .....

    Fonction : Importer les données Json depuis plusieurs fichiers et les regrouper de façon structurer 
               pour faciliter l'utilisation
    """
    files = os.listdir(source)
    question = {}
    for file in files :
        with open("json/{}".format(file), 'r',encoding='utf8') as f:
            datastore = json.load(f)
            if "quests" in datastore :
                    if datastore["quests"] != []:
                        question = _construct(data = datastore,question = question,parent = ['root'],questionnaire_type = questionnaire_type)
    return question

def import_json_file(source):
    """
    Input : PATH du fichier source 

    Output : Dictionnaire dans le format suivant
            
            User1:
                    Type_de_question_1 :
                                        question1
                                        question2
                                        ....
                    Type_de_question_2 :
                                        question1
                                        question2
                                        ....
                    .....

    Fonction : Importer les données Json depuis un fichier et les regrouper de façon structurer 
               pour faciliter l'utilisation
    """
    question = {}
    with open("json/{}".format(source), 'r',encoding='utf8') as f:
        datastore = json.load(f)
        if "quests" in datastore :
            if datastore["quests"] != []:
                question = _construct(datastore,question,['root'],'')
    return question


def fetch_user(querry,question):
    """
    Input : Type de question (string) , Dictionnaire formaté ( avec une des deux fonctions d'importation json )

    Output : dictionnaire.

    Fonction : Compte le nombre de personnes à qui on a pose chaque questions
    """
    Range_personne = {}
    for key in question.keys():
        if querry in question[key] : 
            for el in question[key][querry]:
                if el not in Range_personne :
                    Range_personne[el] = 0

                Range_personne[el]+=1 
    return Range_personne



def fetch_mean(querry,question):
    """
    Input : Type de question (string) , Dictionnaire formaté ( avec une des deux fonctions d'importation json )

    Output : dictionnaire.

    Fonction : Renvoye la moyenne des reponses par questions
    """
    Range_personne = {}
    fetch_U = fetch_user('Range',question)
    for key in question.keys():
        if querry in question[key] : 
            for el in question[key][querry]:
                if el not in Range_personne :
                    Range_personne[el] = 0

                Range_personne[el]+= question[key][querry][el]['value']
    for v in Range_personne.keys():
        Range_personne[v] = Range_personne[v]/fetch_U[v]
    return Range_personne


def unpack(data,title='No title'):
    """
    Input : Un dictionnaire provenant d'une des fonctions fetch , un titre (string)

    Output : graphique 

    Fonction : Afficher un graphique depuis les donnees d'un dictionnaire
    """
    plt.figure(figsize=(3, 20)) 
    plt.barh(*zip(*data.items()))
    plt.title(title)
    plt.show()

def _my_function(x):
    """ 
    Input : Dictionnaire

    Output : Dictionnaire

    Fonction : Retourne un dictionnaire sans ses doublons 
    """
    return  list(set(tuple(element) for element in x))



def retrieve_path(tree):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : List 

    Fonction : Renvoie une list de toutes les root des questions
    """
    path = []
    for personne in tree.keys() :
        #Personne
        for type_q in tree[personne].keys() :
            #Type de question
            if type_q not in ["Checkbox","Radio"] :
                #si question est checkbox ou radio
                for quest in tree[personne][type_q].keys() :
                    # Question
                    root = tree[personne][type_q][quest]['root']
                    path.append(root)

            else : 
                for quest in tree[personne][type_q].keys() :
                    for subelement in tree[personne][type_q][quest].keys():

                        root = tree[personne][type_q][quest][subelement]['root']
                        path.append(root)
    return _my_function(path)


def build_tree(root):
    """
    Input : List (provenant de retrieve_path)

    Output : List/Dictionnaire

    Fonction : Crée un arbre depuis une liste de path  
    """
    J = []
    for path in root :
        parts = path
        parent_list, current_list = J, J

        for index, part in enumerate(parts):
            for item in current_list:
                if part in item and type(item) != str:
                    parent_list, current_list = current_list, item[part]
                    break
            else:
                if index == len(parts) - 1:
                    current_list.append(part)
                else:
                    new_list = []
                    current_list.append({part:new_list})
                    parent_list, current_list = current_list, new_list 
    return J


def recur(arbre,previous_root):
    """
    Input : racine d'arbre (dict/list) , objet_Node (Node)
    
    Fonction : Cree un arbre d'objet Node depuis un abre (List/dict)
    """
    for branche in arbre :
        if type(branche) == str :
            Node(branche,parent = previous_root)
        elif type(branche) == dict :
            for key in branche.keys() :
                tmp = Node(key,parent = previous_root)
                recur(branche[key],tmp) 

def recur_tree(J):
    """
    Input : un arbre (dict/list)

    Output : Objet_Node (Node)

    Fonction : Lance une fonction qui cree un arbre de Node puis retourne la racine de l'arbre
    """
    udo = Node("root",color='red')
    recur(J[0]['root'],udo)
    return udo 

def display_tree(udo):
    """
    Input : racine d'arbre (Node) 
    
    Fonction : Affiche l'arbre entier depuis la racine (Node)
    """
    for pre, fill, node in RenderTree(udo):
     print("%s%s" % (pre, node.name))


def save(udo):
    """
    Input : racine d'arbre (Node)

    Fonction : Sauvegarde l'arbre entier sous format png ( sauvegarde aussi en .dot)
    """
    DotExporter(udo).to_dotfile('udo.dot')
    Source.from_file('udo.dot')
    render('dot', 'png', 'udo.dot') 

def stat_pourc_total(question_list):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste toutes les qestions avec le nombre de fois qu'elle a ete pose / repondu (output1)
               puis la moyenne (repondu/total) repondu  (output2)
    """
    type_question = {}
    for personne in question_list.keys() :
        for el in question_list[personne].keys() :
            if el not in type_question :
                type_question[el] ={}
                type_question[el]['True'] = 0
                type_question[el]['Total'] = 0
            if el not in  ["Checkbox","Radio"] :
                for quest in question_list[personne][el] :
                        if question_list[personne][el][quest]['answered'] == 'true' :
                            type_question[el]['True'] +=1
                        type_question[el]['Total'] += 1
            else :
                for quest in question_list[personne][el] :
                    for subquestion in question_list[personne][el][quest] :
                        if question_list[personne][el][quest][subquestion]['answered'] == 'true' :
                            type_question[el]['True'] +=1
                        type_question[el]['Total'] += 1

    pourc = {}
    for type_q in type_question :
        pourc[type_q] = type_question[type_q]['True']/type_question[type_q]['Total']

    return type_question,pourc


def stat_pourc_unite(question_list):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste les type de questions avec le nombre de fois qu'elles ont ete pose / repondu, par utilisateurs  (output1)
               puis la moyenne (repondu/total) par utilisateur (output2)
    """
    type_question = {}
    for personne in question_list.keys() :
        type_question[personne] = {}
        for el in question_list[personne].keys() :
            if el not in type_question[personne] :
                type_question[personne] [el] ={}
                type_question[personne] [el]['True'] = 0
                type_question[personne] [el]['Total'] = 0
            if el not in  ["Checkbox","Radio"] :
                for quest in question_list[personne][el] :
                        if question_list[personne][el][quest]['answered'] == 'true' :
                            type_question[personne] [el]['True'] +=1
                        type_question[personne] [el]['Total'] += 1
            else :
                for quest in question_list[personne][el] :
                    for subquestion in question_list[personne][el][quest] :
                        if question_list[personne][el][quest][subquestion]['answered'] == 'true' :
                            type_question[personne] [el]['True'] +=1
                        type_question[personne] [el]['Total'] += 1

    pourc = {}
    for personne in type_question :
        pourc[personne]={}
        for type_q in type_question[personne]:
            pourc[personne][type_q] = type_question[personne][type_q]['True']/type_question[personne][type_q]['Total']

    return type_question,pourc


def stat_pourc_unite(question_list):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste les type de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu (output1)
               puis la moyenne  (repondu/total) par utilisateur (output2)
    """
    type_question = {}
    for personne in question_list.keys() :
        type_question[personne] = {}
        for el in question_list[personne].keys() :
            if el not in type_question[personne] :
                type_question[personne] [el] ={}
                type_question[personne] [el]['True'] = 0
                type_question[personne] [el]['Total'] = 0
            if el not in  ["Checkbox","Radio"] :
                for quest in question_list[personne][el] :
                        if question_list[personne][el][quest]['answered'] == 'true' :
                            type_question[personne] [el]['True'] +=1
                        type_question[personne] [el]['Total'] += 1
            else :
                for quest in question_list[personne][el] :
                    for subquestion in question_list[personne][el][quest] :
                        if question_list[personne][el][quest][subquestion]['answered'] == 'true' :
                            type_question[personne] [el]['True'] +=1
                        type_question[personne] [el]['Total'] += 1

    pourc = {}
    for personne in type_question :
        pourc[personne]={}
        for type_q in type_question[personne]:
            pourc[personne][type_q] = type_question[personne][type_q]['True']/type_question[personne][type_q]['Total']

    return type_question,pourc


def stat_pourc_required_unite(question_list):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste les type de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu par utilisateur (output1)
               puis la moyenne  (repondu/total) par utilisateur (output2)
    """
    type_question = {}
    for personne in question_list.keys() :
        type_question[personne] = {}
        for el in question_list[personne].keys() :
            if el not in type_question[personne] :
                type_question[personne] [el] ={}
                type_question[personne] [el]['True'] = 0
                type_question[personne] [el]['Total'] = 0
            if el not in  ["Checkbox","Radio"] :
                for quest in question_list[personne][el] :
                    if question_list[personne][el][quest]['required'] == 'true' :
                        if question_list[personne][el][quest]['answered'] == 'true' :
                            type_question[personne] [el]['True'] +=1
                        type_question[personne] [el]['Total'] += 1
            else :
                for quest in question_list[personne][el] :
                    for subquestion in question_list[personne][el][quest] :
                        #print(question_list[personne][el][quest])
                        if question_list[personne][el][quest][subquestion]['required'] == 'true' :
                            if question_list[personne][el][quest][subquestion]['answered'] == 'true' :
                                type_question[personne] [el]['True'] +=1
                            type_question[personne] [el]['Total'] += 1

    pourc = {}
    for personne in type_question :
        mpourc[personne]={}
        for type_q in type_question[personne]:
            try :
                pourc[personne][type_q] = type_question[personne][type_q]['True']/type_question[personne][type_q]['Total']
            except : 
                pourc[personne][type_q] =0

    return type_question,pourc

def stat_pourc_required_total(question_list):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste les type de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu par utilisateur (output1)
               puis la moyenne  (repondu/total) par utilisateur (output2)
    """
    type_question = {}
    for personne in question_list.keys() :
        for el in question_list[personne].keys() :
            if el not in type_question :
                type_question[el] ={}
                type_question[el]['True'] = 0
                type_question[el]['Total'] = 0
            if el not in  ["Checkbox","Radio"] :
                for quest in question_list[personne][el] :
                    if question_list[personne][el][quest]['required'] == 'true' :
                        if question_list[personne][el][quest]['answered'] == 'true' :
                            type_question[el]['True'] +=1
                        type_question[el]['Total'] += 1
            else :
                for quest in question_list[personne][el] :
                    for subquestion in question_list[personne][el][quest] :
                        #print(question_list[personne][el][quest])
                        if question_list[personne][el][quest][subquestion]['required'] == 'true' :
                            if question_list[personne][el][quest][subquestion]['answered'] == 'true' :
                                type_question[el]['True'] +=1
                            type_question[el]['Total'] += 1

    pourc = {}
    for type_q in type_question:
        try :
            pourc[type_q] = type_question[type_q]['True']/type_question[type_q]['Total']
        except : 
            pourc[type_q] = 0 

    return type_question,pourc


def pourcentage_rep(question_list):
        reponse = {}
        for personne in question_list.keys() :
            tmp_rep = 0
            tmp_total = 0

            for question_type in question_list[personne]:
                if question_type in ["Checkbox","Radio"] :
                    for el in question_list[personne][question_type] :
                        for subquestion in question_list[personne][question_type][el] :
                            if question_list[personne][question_type][el][subquestion ]['answered']== 'true' :
                                tmp_rep +=1
                            tmp_total +=1
                else :
                    for el in question_list[personne][question_type] :
                        if question_list[personne][question_type][el]['answered']== 'true' :
                            tmp_rep +=1
                        tmp_total +=1

            reponse[personne] = tmp_rep
        return reponse 


def question_completion(question_list):

    liste =  {}

    for personne in question_list.keys() :
        liste[personne] = []
        for typeQ in question_list[personne].keys() :

            if typeQ in ["Checkbox","Radio"] :

                for question in question_list[personne][typeQ] :
                    for subquestion in question_list[personne][typeQ][question] : 
                            if question_list[personne][typeQ][question][subquestion]['answered'] == 'true' :
                                ordre = question_list[personne][typeQ][question][subquestion]['ordre']
                                liste[personne].append(ordre)
            else : 
                for question in question_list[personne][typeQ] : 
                    if  question_list[personne][typeQ][question]['answered'] == 'true':
                            ordre = question_list[personne][typeQ][question]['ordre']
                            liste[personne].append(ordre)
    return liste             


def graph_completion(ordre):
    plt.figure(figsize=(20, 20)) 
    oneD = []
    name = []
    endp = []
    endn = []
    for personne in ordre.keys() :
        for index,point in enumerate(sorted(ordre[personne])) :
            
            if index == len(ordre[personne])-1:
                endp.append(point)
                endn.append(personne)
            else :    
                oneD.append(point)
                name.append(personne)

    plt.scatter( oneD ,name , color = 'blue')
    plt.scatter( endp , endn, color = 'red')

    plt.title("representation des questions repondu dans l'ordre")