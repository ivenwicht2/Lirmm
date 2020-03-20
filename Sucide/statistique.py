from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source,render
import numpy as np 
import matplotlib.pyplot as plt



def fetch_mean(question,questionnaire):
    """
    Input : Type de question (string) , Dictionnaire formaté ( avec une des deux fonctions d'importation json )

    Output : dictionnaire.

    Fonction : Renvoye la moyenne des reponses par questions
    """
    fetch_U = {}
    Range_personne = {}
    mm = {}
    for utilisateur in question :
            if questionnaire in question[utilisateur] : 
                for quest in question[utilisateur][questionnaire]['Range'] :
                    if quest not in Range_personne :
                        Range_personne[quest] = 0
                        fetch_U[quest] = 0 
                    fetch_U[quest] += 1
                    Range_personne[quest] += question[utilisateur][questionnaire]['Range'][quest]['value']
                    mm[quest] = {}
                    mm[quest]['min'] = question[utilisateur][questionnaire]['Range'][quest]['min-max'][0]
                    mm[quest]['max'] = question[utilisateur][questionnaire]['Range'][quest]['min-max'][1]

    print(fetch_U)
    for v in Range_personne.keys():
        Range_personne[v] = Range_personne[v]/fetch_U[v]
    return Range_personne , mm

def stat_pourc_total(question,questionnaire):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste toutes les questions avec le nombre de fois qu'elle a ete pose / repondu (output1)
               puis la moyenne (repondu/total) repondu  (output2)
    """
    type_question = {}
    for utilisateur in question :
        if questionnaire in question[utilisateur] :
            for type_quest in question[utilisateur][questionnaire]:
                if type_quest  not in type_question :
                    type_question[type_quest] ={}
                    type_question[type_quest]['True'] = 0
                    type_question[type_quest]['Total'] = 0
                    for quest in question[utilisateur][questionnaire][type_quest] :
                            if question[utilisateur][questionnaire][type_quest][quest]['answered'] == 'true' :
                                type_question[type_quest]['True'] +=1
                            type_question[type_quest]['Total'] += 1
        
    pourc = {}
    for type_quest in type_question :
        pourc[type_quest] = type_question[type_quest]['True']/type_question[type_quest]['Total']

    return type_question,pourc


def stat_pourc_required_total(question,questionnaire):
    """
    Input : Dictionnaire (importer depuis une fonction import_json)

    Output : Dictionnaire , Dictionnaire

    Fonction : Liste les type de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu par utilisateur (output1)
               puis la moyenne  (repondu/total) par utilisateur (output2)
    """
    type_list = {}
    for utilisateur in question :
        if questionnaire in question[utilisateur] :
            for type_quest in question[utilisateur][questionnaire]:
                if type_quest  not in type_list :
                        type_list[type_quest] ={}
                        type_list[type_quest]['True'] = 0
                        type_list[type_quest]['Total'] = 0
                
                for quest in  question[utilisateur][questionnaire][type_quest] :
                        if  question[utilisateur][questionnaire][type_quest][quest]['required'] == 'true' :
                            if  question[utilisateur][questionnaire][type_quest][quest]['answered'] == 'true' :
                                    type_list[type_quest]['True'] +=1
                            type_list[type_quest]['Total'] += 1

    pourc = {}
    for type_q in type_list:
        try :
            pourc[type_q] = type_list[type_q]['True']/type_list[type_q]['Total']
        except : 
            pourc[type_q] = 0 

    return type_list,pourc




def question_completion(question,questionnaire):
    """
        Input : Dictionnaire (importer depuis une fonction import_json), string (reference du questionnaire)

        Output : liste de question repondu/pas repondu (le signe | est présent avant est après chaque question non repondu )

        Fonction : liste les questions repondu ou non par utilisateur
    """
    liste =  {}

    for utilisateur in question :
        if questionnaire in question[utilisateur] :
            liste[utilisateur] = {}
            tmp = []
            for type_quest in question[utilisateur][questionnaire]:
                for quest in question[utilisateur][questionnaire][type_quest] :
                    if question[utilisateur][questionnaire][type_quest][quest]['answered'] == 'true' :
                        ordre = question[utilisateur][questionnaire][type_quest][quest]['ordre']
                        tmp.append(ordre)
                    else  : 
                        ordre = question[utilisateur][questionnaire][type_quest][quest]['ordre']
                        tmp.append('|'+str(ordre)+'|')
                liste[utilisateur] = tmp


    return liste 



def pourcentage_rep(question,questionnaire):
    """
    
    """
    reponse = []
    for utilisateur in question :
        if questionnaire in question[utilisateur] :
            tmp_rep = 0
            tmp_total = 0
            for type_quest in question[utilisateur][questionnaire]:
                    for quest in question[utilisateur][questionnaire][type_quest] :
                            if question[utilisateur][questionnaire][type_quest][quest]['answered']== 'true' :
                                tmp_rep +=1
                            tmp_total += 1
                    reponse.append(tmp_rep/tmp_total)

    return  np.mean(reponse) , len(reponse)



def niveau_ids_total(question,questionnaire,hierarchy):
    liste={}
    for utilisateur in question :
        if questionnaire in question[utilisateur] :
            for quest in question[utilisateur][questionnaire]['Range'] :
                if quest not in liste and quest in hierarchy:
                    liste[quest] = []
                if quest in hierarchy and 'value' in question[utilisateur][questionnaire]['Range'][quest]:
                    liste[quest].append(question[utilisateur][questionnaire]['Range'][quest]['value'] )
    liste_mean = {}
    for key in liste:
        liste_mean[key] = np.mean(liste[key])
    return liste_mean


def question_test(question,questionnaire,question1,question2,val):
    liste = []
    for utilisateur in question :
        tmp = None
        if questionnaire in question[utilisateur] :
            requirement = False 
            for quest in question[utilisateur][questionnaire]['Range']:
                if  quest == question2 :
                    tmp =  question[utilisateur][questionnaire]['Range'][quest]['value']

                if quest == question1 :
                    if question[utilisateur][questionnaire]['Range'][quest]['value'] >= val :
                        requirement = True
                    
                        
                if requirement == True and tmp != None: 
                    liste.append(tmp)
    return np.mean(liste),len(liste)



