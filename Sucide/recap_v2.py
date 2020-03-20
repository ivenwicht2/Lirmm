from statistique import *
from pipeline import * 
import matplotlib.pyplot as plt

class stat_json():
    def __init__(self,path):
        self.path = path
        self.data =  import_json(self.path)
        self._questionnaire = self._fetch_questionnaire()
        self.hierarchy={}
        self.hierarchy['IDS'] = 'root'
        self.hierarchy['q3_intensite_tuer'] = 'IDS'
        self.hierarchy['intens_moy_tuer'] = 'IDS'
        self.hierarchy['idees_suicidaires_moyen'] = 'IDS'
        self.hierarchy['q2_intens_idees_suicid'] = 'IDS'
        self.hierarchy['intensite_idee_suicide'] = 'IDS'
        self.hierarchy['q21_me_faire_mal_metuer'] = 'IDS'
        self.hierarchy['intensite_intention_suicide'] = 'IDS'

    def _fetch_questionnaire(self):
        liste_questionnaire = []
        for utilisateur in self.data :
            for questionnaire in self.data[utilisateur]:
                if questionnaire not in liste_questionnaire :
                    liste_questionnaire.append(questionnaire)
        return liste_questionnaire

    
    def _Treponse(self):
        graph = {}
        for questionnaire in self._questionnaire :
            type_question,pourc = stat_pourc_total(self.data,questionnaire)
            keys = [ el for el in type_question.keys()]
            graph[questionnaire] = pourc
        return graph

    def fetch_mean(self):
        """
        Moyenne des reponses ( pour le type de question range ) par question par questionnaire 
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire)
            mean,mm = fetch_mean(self.data,questionnaire)
            for key in mean :
                print("{} : {} , {}".format(key,mean[key],mm[key]))

    def required(self):
        """
        Output :  Liste toutes les types de questions obligatoire avec le nombre de fois qu'elles ont ete pose / repondu et pourcentage
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire)     
            type_question,pourc= stat_pourc_required_total(self.data,questionnaire)
            for key in type_question :
                print("{} : {} pourcentage : {}".format(key,type_question[key],pourc[key]))
            print()


    def ordre(self):
        """
        Liste des questions repondu par questionnaires par utilisateurs 
        """
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire)
            ordreQ =  question_completion(self.data,questionnaire)
            for key in ordreQ:
                print("{} :".format(key),end='')
                for el in  ordreQ[key] :
                    print('{} '.format(el),end='')
                print()
            print()

    def _pourc_rep(self):
        """
        Pourcentage de question repondu par questionnaires par utilisateurs 
        """
        graph = {}
        for questionnaire in self._questionnaire :
            pourc_rep,size = pourcentage_rep(self.data,questionnaire)
            graph[questionnaire] = [pourc_rep,size]
        return graph

    def ids_total(self):
        liste = None 
        for questionnaire in self._questionnaire :
            print('*'*5,end='')
            print(questionnaire)
            liste = niveau_ids_total(self.data,questionnaire,self.hierarchy)
            for key in liste :
                print("{} : {} ".format(key,liste[key]))
            print()

    def comp(self,quest1,quest2,val_quest1):
        liste = None 
        for questionnaire in self._questionnaire :
            moyenne,taille = question_test(self.data,questionnaire,quest1,quest2,val_quest1)
            if str(moyenne) != "nan" :
                print('*'*5,end='')
                print(questionnaire)
                print('moyenne : ',moyenne ,' taille échantillions : ', taille)

    def log(self):
        data = log_extract(self.path)
        plt.title("Graphique du taux de connection en fonction de l'heure")
        plt.plot(list(data.keys()), list(data.values()),'ro')
        plt.grid(True)


    def display_pourc_rep(self,element):
        data = self._pourc_rep()
        
        y1 = []
        y2 = []
        for questionnaire in data :
            if questionnaire.find(element) > -1 :
                y1.append(data[questionnaire][0])
                y2.append(data[questionnaire][1])
        x1 = [i for i in range(len(y1))]
        x2 = [i for i in range(len(y2))]

        
        fig, ax1 = plt.subplots(figsize=(15, 5))
        color = 'tab:red'
        ax1.set_xlabel('questionnaire')
        ax1.set_ylabel('pourcentage de reponse', color=color)
        ax1.plot(x1, y1, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel("nombre d'utilisateur", color=color)  
        ax2.plot(x2, y2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        

        plt.sca(ax1)
        plt.xticks(x1, [element+"_{}".format(i) for i in range(len(x1)) ], rotation='vertical')
        plt.grid(True)

    def display_Treponse(self,element):
        data = self._Treponse()
        b1,b2,b3,b4,b5 = [],[],[],[],[]
        for questionnaire in data :
            if questionnaire.find(element) > -1 :
                for typeQ in data[questionnaire]:
                    if typeQ == 'Range' : b1.append(data[questionnaire][typeQ])
                    if typeQ == 'Radio' : b2.append(data[questionnaire][typeQ])
                    if typeQ == 'Checkbox' : b3.append(data[questionnaire][typeQ])
                    if typeQ == 'YesNo' : b4.append(data[questionnaire][typeQ])
                    if typeQ == 'Text' : b5.append(data[questionnaire][typeQ])
        barWidth = 1
        r1,r2,r3,r4,r5 = [],[],[],[],[]
        pred = 0
        for i in range(np.max([len(b1),len(b2),len(b3),len(b4),len(b5)])):
            r1.append(pred+barWidth)
            pred = pred+barWidth
            r2.append(pred+barWidth)
            pred = pred+barWidth
            r3.append(pred+barWidth)
            pred = pred+barWidth
            r4.append(pred+barWidth)
            pred = pred+barWidth
            r5.append(pred+barWidth)
            pred += 5

        plt.figure(figsize=(10, 5))
        plt.bar(r1, b1, color='red', width=barWidth, edgecolor='white', label='Range')
        plt.bar(r2, b2, color='green', width=barWidth, edgecolor='white', label='Radio')
        plt.bar(r3, b3, color='grey', width=barWidth, edgecolor='white', label='CheckBox')
        plt.bar(r4, b4, color='brown', width=barWidth, edgecolor='white', label='YesNo')
        plt.bar(r5, b5, color='black', width=barWidth, edgecolor='white', label='Text')

        plt.xticks([r + barWidth for r in r1], [element+"_{}".format(i) for i in range(len(b1)) ], rotation='vertical')
        plt.gca().legend(bbox_to_anchor=(1,0.5), loc='center left')

        plt.show()

    def week_use(self):
        data = log_week_extract(self.path)
        plt.title("Graphique du taux de connection en fonction de la semaine")
        plt.bar(list(data.keys()), list(data.values()))
        plt.xticks([0,1,2,3],["week_{}".format(i) for i in range(1,5) ])
            

