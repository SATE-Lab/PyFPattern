

def paginated_response(self, func, result_key=''):
    "\n        Returns expanded response for paginated operations.\n        The 'result_key' is used to define the concatenated results that are combined from each paginated response.\n        "
    args = dict()
    results = dict()
    loop = True
    while loop:
        response = func(**args)
        if (result_key == ''):
            result = response
            result.pop('ResponseMetadata', None)
        else:
            result = response.get(result_key)
        results.update(result)
        args['Marker'] = response.get('NextMarker')
        for key in response.keys():
            if key.endswith('List'):
                args['Marker'] = response[key].get('NextMarker')
                break
        loop = (args['Marker'] is not None)
    return results
