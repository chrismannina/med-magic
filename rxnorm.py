# Description: CS361 project - RxNorm API from the National Library of Medicine with current CLI UI
# Author: Chris Mannina
# Disclaimer: "This product uses publicly available data from the U.S. National Library of Medicine (NLM), National
# Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not
# endorse or recommend this or any other product."

import requests
import json

def get_drug_info(drug_name):
    """
    Using RxNorm API getApproximateMatch. Searches for strings in the RxNorm data set that most closely match the term
    parameter.
    Function: getApproximateMatch
    Information returned: Concept and atom IDs approximately matching a query
    HTTP GET request: https://rxnav.nlm.nih.gov/REST/approximateTerm.xml?term=value&maxEntries=value&option=value
    :param med_name: string, of which to find approximate matches (HTTP req param = term)
    :return: results of NLM RxNorm query (output as JSON)
    """

    # HTTP get request -> response object called r
    r = requests.get('https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term=' + drug_name + '&maxEntries=1')
    # check if got an error
    if r.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(r.status_code))

    # store json results: rxcui=RxNorm identifier, rxaui=RxNorm RXAUI (string identifier) that matches,
    # score=Match score (higher is better), rank=1 for all best matches, 2 for all second-best matches, etc.
    drug_info = r.json()
    score = []
    rxcui = []
    properties = []
    # when multiple results (currently set to 1)
    try:
        for i in drug_info['approximateGroup']['candidate']:
            score.append(i['score'])
            rxcui.append(i['rxcui'])
            get_properties = get_all_properties(i['rxcui'])
            properties.append(get_properties)
    except:
        return

    return properties, score


def get_all_properties(rxcui):
    """
    Using RxNorm API getAllProperties. Return certain categories of properties for the RxNorm concept specified by
    rxcui. Information returned includes property name, value and category. The prop parameter selects the categories
    of properties to retrieve.
    Function: getAllProperties
    Information returned: Concept details
    HTTP GET request: https://rxnav.nlm.nih.gov/REST/rxcui/rxcui/allProperties.xml?prop=yourPropCategories
    :param rxcui: rxcui identifier.
    :return: json result of all properties for that rxcui
    """

    # HTTP get request -> response object called r
    r = requests.get('https://rxnav.nlm.nih.gov/REST/rxcui/' + rxcui + '/allProperties.json?prop=all')
    # check for error
    if r.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(r.status_code))
    return r.json()


if __name__ == '__main__':
    # welcome message in CLI for user
    print('Welcome to the drug finder. Here you can enter a enter a drug name and dose (e.g. Atenolol 50 mg), and the '
          'program will search the National Library of Medicine for the closest match.\n')
    # loop begins
    loop = 'y'
    while loop.lower() == 'y':
        # user inputs drug name
        drug_name = input('Please enter a drug name: \n')
        print(f'Querying the National Library of Medicine for a match on {drug_name}.\n')
        # get results from API
        try:
            rx_data, score = get_drug_info(drug_name)
            # print results of match for user
            for i in range(len(rx_data)):
                print('\n')
                print(f'*** RxNorm Match {i + 1} ***')
                print('Match Score = ', score[i], '(higher indicates better)')
                for j in range(len(rx_data[i]['propConceptGroup']['propConcept'])):
                    # if rx_data[i]['propConceptGroup']['propConcept'][j]['propName'] != "NDA":
                    print(rx_data[i]['propConceptGroup']['propConcept'][j]['propName'], "=",
                          rx_data[i]['propConceptGroup']['propConcept'][j]['propValue'])
        except:
            print('No match found')

        # user input to search again
        loop = input('Would you like to search another drug? [y/n]: \n')

