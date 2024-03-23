import requests

response = requests.post('http://127.0.0.1:5000/advert/',
                         json={'title': 'The AI is attacking!',
                               'description': 'AI attacked people!',
                               'owner': 'TRUE!'}
                         )
#
# response = requests.get('http://127.0.0.1:5000/advert/1/')
#
# response = requests.patch('http://127.0.0.1:5000/advert/1/',
#                           json={'title': 'The AI is attacking again!',
#                                 'description': 'HELP!',
#                                 'owner': 'LIE!'}
#                           )
# response = requests.delete('http://127.0.0.1:5000/advert/1/')
# response = requests.get('http://127.0.0.1:5000/advert/1/')
print(response.status_code)
print(response.text)
