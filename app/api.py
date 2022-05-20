# Description: CS361 project - RxNorm API from the National Library of Medicine with current CLI UI
# Author: Chris Mannina
# Disclaimer: "This product uses publicly available data from the U.S. National Library of Medicine (NLM), National
# Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not
# endorse or recommend this or any other product."

from unicodedata import category
import requests
import json


def rxnorm(query):
    """Main function to search for a medication in RxNorm."""
    try:
        data = get_approximate_match(query)
        res = get_all_properties(data)
        return res
    except:
        raise Exception('No match found (rxnorm)')
    

def get_approximate_match(term):
    """
    RxNorm API = getApproximateMatch
    Searches for strings in the RxNorm data set that most closely match the term
    parameter. Returns concept and atom IDs approximately matching a query.
    HTTP GET request: https://rxnav.nlm.nih.gov/REST/approximateTerm.xml?term=value&maxEntries=value&option=value
    :param term: string of which to find approximate matches (HTTP req param = term)
    :return: results of NLM RxNorm query (output as JSON)
    """
    rxcui = []
    data = {}
    try:
        # HTTP get request -> response object called res
        r = requests.get('https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=' + term + '&maxEntries=1')
        # check if got an error
        if r.status_code != 200:
            raise Exception('Response code 200')
    except:
        # no match found -> print a message to console and return a Nont object
        raise Exception('No match found (getApproximateMatch)')
    # store json results: rxcui=RxNorm identifier, rxaui=RxNorm RXAUI (string identifier) that matches,
    # score=Match score (higher is better), rank=1 for all best matches, 2 for all second-best matches, etc.
    candidate = r.json()
    for group in candidate['approximateGroup']['candidate']:
        if group['rxcui'] not in rxcui:
            rxcui.append(group)
            data[group['rxcui']] = {}
            data[group['rxcui']] = group  
    return data

def get_all_properties(data): 
    """
    Using RxNorm API getAllProperties. Return certain categories of properties for the RxNorm concept specified by
    rxcui. Information returned includes property name, value and category. The prop parameter selects the categories
    of properties to retrieve.
    Function: getAllProperties
    Information returned: Concept details
    HTTP GET request: https://rxnav.nlm.nih.gov/REST/rxcui/rxcui/allProperties.xml?prop=yourPropCategories
    :param data: dicitionary with keys 0...n. Access rxcui identifier -> n['rxcui'] .
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
                # todo: add a class exception
                raise Exception('Response code 200')        
            concept = r.json()
            category = None
            for group in concept['propConceptGroup']['propConcept']:
                if not category == group['propName']:
                    # changing variable to current propName so we don't continually reiterate over that data
                    category = group['propName']
                    properties[key][group['propName']] = group['propValue']  
    return properties


if __name__ == '__main__':
    # CLI if app run alone
    print('Welcome to the drug finder. Here you can enter a enter a drug name and dose (e.g. Atenolol 50 mg), and the '
          'program will search the National Library of Medicine for the closest match.\n')
    loop = 'y'
    while loop.lower() == 'y':
        query = input('Please enter a drug name: \n')
        print(f'Querying the National Library of Medicine for a match on {query}.\n')
        try:
            data = rxnorm(query)
            print('*** RxNorm Match ***')
            print('Here is result from approximate term query: ', data)
        except:
            print('No match found - Main')
        # user input to search again
        loop = input('Would you like to search another drug? [y/n]: \n')

