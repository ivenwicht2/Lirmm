
from jsontools import * 

class questionnaire():
    def __init__(self,path,typeQ):
        self.data = import_json(path,typeQ)
        self.nom = typeQ



class stat_json():

    def __init__(self,path):
        self._questionnaire =  [questionnaire(path,"Hebdomadaire")]
        self._questionnaire.append(questionnaire(path,"Mensuel"))
        self._questionnaire.append(questionnaire(path,"EMMA"))
        self._questionnaire.append(questionnaire(path,"Socio-démographique"))
        self.hierarchy={}
        self.hierarchy['IDS'] = 'root'
        self.hierarchy['q3_intensite_tuer'] = 'IDS'
        self.hierarchy['intens_moy_tuer'] = 'IDS'
        self.hierarchy['idees_suicidaires_moyen'] = 'IDS'
        self.hierarchy['q2_intens_idees_suicid'] = 'IDS'
        self.hierarchy['intensite_idee_suicide'] = 'IDS'
        self.hierarchy['q21_me_faire_mal_metuer'] = 'IDS'
        self.hierarchy['intensite_intention_suicide'] = 'IDS'

    def Arbre(self):
        """
        Output : Arbre des questions pour chaque type de questionnaire
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            question = retrieve_path(questionnaire.data)
            tree = build_tree(question)
            tree_object = recur_tree(tree)
            display_tree(tree_object)
            print()

    def Treponse(self):
        """
        Output :  Liste toutes les types de questions avec le nombre de fois qu'elles ont ete pose / repondu et pourcentage
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            type_question,pourc = stat_pourc_total(questionnaire.data)
            keys = [ el for el in type_question.keys()]
            for key in keys :
                print("{} : {} pourcentage : {}".format(key,type_question[key],pourc[key]))

    def fetch_mean(self):
        """
        Moyenne des reponses ( pour le type de question range ) par question par questionnaire 
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            mean,mm = fetch_mean('Range',questionnaire.data)
            for key in mean.keys() :
                print("{} : {} , {}".format(key,mean[key],mm[key]))

    def ordre(self):
        """
        Liste des questions repondu par questionnaires par utilisateurs 
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            ordreQ =  question_completion(questionnaire.data)
            for key in ordreQ.keys():
                print("{} :".format(key),end='')
                for el in  ordreQ[key] :
                    print('{} '.format(el),end='')
                print()
            print()

    def pourc_rep(self):
        """
        Pourcentage de question repondu par questionnaires par utilisateurs 
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            pourc_rep = pourcentage_rep(questionnaire.data)
            for key in pourc_rep.keys():
                print('{} : {}'.format(key , pourc_rep[key]))
            return pourc_rep
            print()

    def required(self):
        """
        Output :  Liste toutes les types de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu et pourcentage
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)     
            type_question,pourc= stat_pourc_required_total(questionnaire.data)
            for key in type_question.keys() :
                print("{} : {} pourcentage : {}".format(key,type_question[key],pourc[key]))
            return pourc
            print()

    def ids_unique(self):
                
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            liste = niveau_ids_unique(questionnaire.data,self.hierarchy)
            for key in liste.keys() :
                print("{} : {}".format(key,liste[key]))
            print()
    
    def ids_total(self):
        liste = None 
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire.nom)
            liste = niveau_ids_total(questionnaire.data,self.hierarchy)
            for key in liste.keys() :
                print("{} : {} ".format(key,liste[key]))
            print()


     