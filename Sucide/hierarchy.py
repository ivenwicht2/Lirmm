hierarchy={}
hierarchy['IDS'] = 'root'
hierarchy['q3_intensite_tuer'] = 'IDS'
hierarchy['intens_moy_tuer'] = 'IDS'
hierarchy['idees_suicidaires_moyen'] = 'IDS'
hierarchy['q2_intens_idees_suicid'] = 'IDS'
hierarchy['intensite_idee_suicide'] = 'IDS'
hierarchy['q21_me_faire_mal_metuer'] = 'IDS'
hierarchy['intensite_intention_suicide'] = 'IDS'

hierarchy['agitation'] = 'root'
hierarchy['agitation_tension_emotionnelle_maximum'] = 'agitation'
hierarchy['q8_agitation_tension_hebdo'] = 'agitation'
hierarchy['q8_emma_agitation'] = 'agitation'

hierarchy['douleurs'] = 'root'
hierarchy['q5_emma_douleur_morale'] = 'douleurs'
hierarchy['douleur_morale_moyen'] = 'douleurs'
hierarchy['q1_douleur_psy'] = 'douleurs'
hierarchy['douleurs_psy_tolerance'] = 'douleurs'
hierarchy['douleurs_max'] = 'douleurs'

hierarchy['other'] = 'root'
hierarchy['matin_bien_dormi'] = 'other'
hierarchy['jour_qualite_appetit'] = 'other'
hierarchy['bien_etre'] = 'other'

hierarchy['phone_calls'] = 'root'
hierarchy['AppelCentre'] = "phone_calls"
hierarchy['Appel15'] = "phone_calls"
hierarchy['AppelProche'] = "phone_calls"
hierarchy['smsArrived'] = "phone_calls"
hierarchy['AppelUrgence'] = "phone_calls"

hierarchy['emotion_regulation'] = 'root'
hierarchy['exrelax'] = "emotion_regulation" 
hierarchy['photoopen'] = "emotion_regulation"
hierarchy['musicplay'] = "emotion_regulation"
hierarchy['diaporama'] = "emotion_regulation"

hierarchy['actions'] = 'root'
hierarchy['login'] = 'actions'
hierarchy['ForgetMDP'] = 'actions'

hierarchy_keys = []
hierarchy_leaves = []
for key in hierarchy:
    if (hierarchy[key] == 'root'):
        hierarchy_keys.append(key)
    else:
        hierarchy_leaves.append(key)

        
# Binary attributes
binary_question={}
binary_question['AppelCentre'] = "phone_calls"
binary_question['Appel15'] = "phone_calls"
binary_question['AppelProche'] = "phone_calls"
binary_question['exrelax'] = "emotion_regulation" 
binary_question['smsArrived'] = "phone_calls"
binary_question['AppelUrgence'] = "phone_calls"
binary_question['photoopen'] = "emotion_regulation"
binary_question['musicplay'] = "emotion_regulation"
binary_question['diaporama'] = "emotion_regulation"
binary_question['login'] = "actions"
binary_question['ForgetMDP'] = "actions"

binary_question_key = binary_question.keys

