from pyramid.view import view_config
import json
from pyramid.response import Response
import pandas as pd
import numpy as np


@view_config(route_name='benford', renderer='json', request_method='POST')
def benford(request):

    # get the uploaded file
    uploaded_file = request.POST['file'].file
    
    
    # read the file using pandas
    df = pd.read_csv(uploaded_file)
    print(df)
   
    # get the first digit of each number in the file
    df['first_digit'] = df.iloc[:, 0].astype(str).str[0]
    first_digits= df['first_digit'].value_counts()
    first_digits_dict = first_digits.to_dict()
    print(first_digits_dict)

    # calculating the observer frequency
    observerd_frequency_dict = {k: first_digits_dict[k]/sum(first_digits_dict.values()) for k in first_digits_dict.keys()}
    print(observerd_frequency_dict)

    # calculate the expected frequencies according to Benford's law
    expected_freq = {str(k): np.log10(1+(1/k)) for k in range(1,10)}
    print("===========================")
    print(expected_freq)
    
    # finding the order of keys in expected and observerd frequency
    expected_order = list(expected_freq.keys())
    observed_order = list(observerd_frequency_dict.keys())

    print(expected_order)
    print(observed_order)

    if expected_order == observed_order:
        response_data = {"status": "success", "message": "The dataset supports benfords law."}
        response = Response(json.dumps(response_data), content_type='application/json; charset=utf-8', status=200)
        return response
    else:
        # calcualting the keys with max fre4quenxy for observed and expected frequency
        observed_max = max(observerd_frequency_dict, key=observerd_frequency_dict.get)
        expected_max = max(expected_freq, key=expected_freq.get)
        if observed_max==expected_max:
            response_data = {"status": "success", "message": "The dataset supports benfords law."}
            response = Response(json.dumps(response_data), content_type='application/json; charset=utf-8', status=200)
            return response
        else:
            response_data = {"status": "error", "message": "The dataset doesn't supports benfords law."}
            response = Response(json.dumps(response_data), content_type='application/json; charset=utf-8', status=400)
            return response
    

   

@view_config(route_name='home', renderer='templates/home.html')
def home(request):
    return { 'name': 'Pyramid1' }