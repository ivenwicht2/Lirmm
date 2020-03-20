import json
import os
import datetime


def import_json(path):
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
    files = os.listdir(path)
    question = {}
    for file in files :
        with open("json/{}".format(file), 'r',encoding='utf8') as f:
            datastore = json.load(f)
            user = file.split('.')[0]
            question[user] = {}
            name = []
            if "quests" in datastore :
                    if datastore["quests"] != []:
                        racine = datastore["quests"]
                        start_date = start(racine)
                        if start_date != -1 :
                            for branch in racine :
                                if date(start_date,branch) :
                                    tmp_name = name_attribution(branch,name)
                                    name.append(tmp_name)
                                    question[user][tmp_name] =  pipe(branch["dataquestionnaire"])
    return question                           
                                


def name_attribution(branche,name):
    new_name =  branche["denom"]

    i = 1
    while (new_name in name) :
        new_name = branche["denom"] + '_{}'.format(i)
        i+=1

    return new_name

def start(racine):
    for i in range(len(racine)):
        if racine[i]['type'] == "Socio-démographique" :
            time =  racine[i]['datedue']
            try :
                date_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(days=+30)
                return date_time
            except :
                return -1
  

def date(start,branch):
    time =  branch['datedue']
    try :
        date_time_2 =  datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if start >= date_time_2:
            return True
        else :
                return False
    except :
            return False

def pipe(branch, root=['root'] , ordre = -1):

    extraction = {}
    for element in branch:
        ordre += 1

        typeQ = element['answerType']
        if typeQ not in extraction :
            extraction[typeQ] = {}

        if typeQ == "Range":
            if 'required' in element : 
                required = 'true'
            else : 
                required = 'false' 

            if 'sousquest' in element['options'] :
                extraction[typeQ][element['code']] = {
                    'value' : element['value'],
                    'subtitle':element['subtitle'],
                    'answered':element['answered'],
                    'min-max' : [element['options']['min'] ,element['options']['max']],
                    'root' : root,
                    'required':required,
                    'ordre':ordre}  

                root.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    tmp = pipe(branch = [subquestion] , root = root ,ordre=ordre)
                    extraction = rec_merge1(extraction,tmp)
                    ordre += 1
            else :
                extraction[typeQ][element['code']] = {
                    'value' : element['value'],
                    'answered':element['answered'],
                    'min-max' : [element['options']['min'] ,element['options']['max']],
                    'root':root,
                    'required':required,
                    'ordre':ordre}

        if typeQ == "Radio" :
            root.append(element['code'])
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            extraction[typeQ][element['code']]= {
                    'answered':element['answered'],
                    "root": root,
                    'required':required,
                    'ordre':ordre}


        if typeQ == 'Checkbox' :
            root.append(element['code'])
            if 'required' in element  : 
                required = 'true'
            else :
                required = 'false'
            extraction[typeQ][element['code']]= {
                    'answered':element['answered'],
                    "root": root,
                    'required': required,
                    'ordre': ordre}


        if typeQ == 'Text' :
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            extraction[typeQ][element['code']] = {
                'value' : element["value"],
                'answered':element['answered'],
                'root' : root,
                'required': required,
                'ordre': ordre
                }

        if typeQ == 'YesNo':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            if 'sousquest' in element['options'] :
                extraction[typeQ][element['code']] = {
                    'value' : element['checked'],
                    'answered':element['answered'],
                    'subquestion_name' : {element['options']['sousquest'][0]['code']},
                    'subquestions':{},
                    'subtitle' :element['options']['sousquest'][0]['subtitle'],
                    'root' : root,
                    'required':required,
                    'ordre':ordre}
                
                root.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    tmp = pipe(branch = [subquestion] , root = root ,ordre=ordre)
                    extraction = rec_merge1(extraction,tmp)
                    ordre += 1

            else :
                extraction[typeQ][element['code']] = {
                    'value' : element['checked'],
                    'answered':element['answered'],
                    'root' : root,
                    'required':required,
                    'ordre':ordre }

        if typeQ == 'Contact':
            if 'required' in element: 
                required = 'true'
            else :
                required = 'false'

            extraction[typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : root,
                'required':required,
                'ordre':ordre}
        
        if typeQ == 'Time':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            extraction[typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : root,
                'required':required,
                'ordre':ordre }

        
        if typeQ == 'Input':
            if 'required' in element : 
                required = 'true'
            else :
                required = 'false'
            extraction[typeQ][element['code']] = {
                'subtitle' : element['subtitle'],
                'value' : element['value'],
                'answered':element['answered'],
                'root' : root,
                'required':required,
                'ordre':ordre }

        if typeQ == 'Section':
            if 'required' in element: 
                required = 'true'
            else :
                required = 'false'
            if 'sousquest' in element['options'] :
                extraction[typeQ][element['code']] = {
                    'subtitle' :element['subtitle'],
                    'answered':element['answered'],
                    'root' : root,
                    'required':required,
                    'ordre':ordre }

                root.append(element['code'])
                for subquestion in element['options']['sousquest'] :
                    tmp = pipe(branch = [subquestion] , root = root ,ordre=ordre)
                    extraction = rec_merge1(extraction,tmp)
                    ordre += 1

    return extraction


def rec_merge1(d1, d2):
    for k, v in d1.items(): 
        if k in d2:
            d2[k] = rec_merge1(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def log_extract(path):
    files = os.listdir(path)
    liste = {}
    for file in files :
        with open("json/{}".format(file), 'r',encoding='utf8') as f:
            datastore = json.load(f)
        if datastore["logs"]  != []:
            for log in datastore["logs"] :
                if log['action'] == "login" :
                    time = log["data"]
                    try :
                        date_time =  datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
                        if date_time.hour not in liste :
                            liste[date_time.hour] = 0
                        liste[date_time.hour] += 1
                    except :
                        pass


    return liste 


def log_week_extract(path):
    files = os.listdir(path)
    liste = {}
    start = 0
    for file in files :
        with open("json/{}".format(file), 'r',encoding='utf8') as f:
            datastore = json.load(f)
        if datastore["logs"]  != []:
            liste[file] = []
            for index,log in enumerate(datastore["logs"]) :
                    time = log["data"]
                    try :
                        date_time =  datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
                        liste[file].append(date_time.isocalendar()[1])
                    except Exception as e:
                        print(e)
    sorted_liste = {}
    for utilisateur in liste: 
        minimum = min(liste[utilisateur])
        for week in liste[utilisateur]:
            if  abs(minimum-week) < 4:
                if abs(minimum-week) not in sorted_liste :
                    sorted_liste[abs(minimum-week)] = 0
                sorted_liste[abs(minimum-week)] +=1
    return sorted_liste
