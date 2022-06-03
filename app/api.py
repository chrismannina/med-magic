import requests


def rxnorm(query, api):
    """
    Main function to search for a medication in RxNorm.
    :param query: search term
    :param api: search function selected 
    :return: results of NLM RxNorm query (output as JSON)
    """
    try:
        if api == 'getDrugs':
            return get_drugs(query)   
        elif api == 'getApproximateMatch':
            data = get_approximate_match(query)
            return get_all_properties(data)
    except:
        raise Exception('No match found (rxnorm)')
    
def get_drugs(name):
    """
    RxNorm API: getDrugs -> get the drug products associated with a specified name.
    :param name: string that can be name of an ingredient, brand name, clinical dose form, branded dose form, clinical 
    drug component, or branded drug component
    :return: list with results of NLM RxNorm query
    """
    try:
        # HTTP get request -> response object called res
        r = requests.get('https://rxnav.nlm.nih.gov/REST/drugs.json?name=' + name)
        if r.status_code != 200:
            raise Exception('Response code 200')
        data = r.json()
        rxcui = []
        drugs = []
        for group in data['drugGroup']['conceptGroup']:
            if 'conceptProperties' in group.keys():
                for drug in group['conceptProperties']:
                    if drug['rxcui'] not in rxcui:
                        rxcui.append(drug['rxcui'])
                        drugs.append(drug) 
        return drugs
    except:
        raise Exception('No match found (getApproximateMatch)')

def get_approximate_match(term):
    """
    RxNorm API: getApproximateMatch -> searches for strings in the RxNorm data set that most closely match the term
    parameter. 
    :param term: string of which to find approximate matches
    :return: dictionary of results of NLM RxNorm query
    """
    try:
        r = requests.get('https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=' + term + '&maxEntries=1')
        # check if got an error
        if r.status_code != 200:
            raise Exception('Response code 200')
        candidate = r.json()
        rxcui = []
        data = {}
        for group in candidate['approximateGroup']['candidate']:
            if group['rxcui'] not in rxcui:
                rxcui.append(group)
                data[group['rxcui']] = {}
                data[group['rxcui']] = group  
        return data
    except:
        raise Exception('No match found (getApproximateMatch)')

def get_all_properties(data): 
    """
    RxNorm API: getAllProperties -> get property name, value and category for given rxcui 
    :param data: dicitionary with keys 0...n. Access rxcui identifier -> n['rxcui']
    :return: json result of all properties for that rxcui
    """
    rxcui = []
    properties = {}
    for key in data.keys():
        if key not in rxcui:
            # only add properties nested dict for new rxcui
            rxcui.append(key)
            properties[key] = {}
            # save query score
            properties[key]['score'] = data[key]['score']
            # get properties from rxcui API req -> store concept from GET req
            r = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui/' + str(key) + '/allProperties.json?prop=all')
            # check for error
            if r.status_code != 200:
                raise Exception('Response code 200')        
            concept = r.json()
            category = None
            for group in concept['propConceptGroup']['propConcept']:
                if not category == group['propName']:
                    # changing variable to current propName so we don't continually reiterate over that data
                    category = group['propName']
                    properties[key][group['propName']] = group['propValue']  
    return properties
