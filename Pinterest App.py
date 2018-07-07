import json,requests


def login():

    #API URL needed for token genration
    callback_uri = "https://www.getpostman.com/oauth2/callback"
    authorize_url = " https://api.pinterest.com/oauth/"
    token_url = "https://api.pinterest.com/v1/oauth/token"

    #Application ID
    client_id = '4976394662544684664'
    client_secret = '993ce5eb11f8a327f9c4cc1145178d9e7eb1be85ecb73eb8071edcf916ed11a4'

    #'''
    #URL for getting user permission
    authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri='  +  callback_uri  + '&scope=read_public'

    print  "Enter following url on the browser and enter the code from the returned url: "
    print  "    " + authorization_redirect_url + "  "
    authorization_code = raw_input('\ncode: ') #getting authorization code from user

    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
    print  "\nrequesting access token"

    # request for getting token
    access_token_response = requests.post("https://api.pinterest.com/v1/oauth/token?grant_type=authorization_code&client_id=" + client_id +"&client_secret="+ client_secret+"&code="+authorization_code )

    #print  "response"
    #print access_token_response
    #print  access_token_response.headers
    #print  'body: ' + access_token_response.text

    # extracting token from response
    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']

    #'''
    #access_token = "Ab_XqpcR44ROEZANtK6tJgmlKeX6FT7bHkPQDQ5FD1BABcA2zAAAAAA"
    print  "\naccess token: " + access_token

    information_url="https://api.pinterest.com/v1/me/?access_token="+access_token +"&fields=id%2Curl%2Cusername"
    board_url = "https://api.pinterest.com/v1/me/boards/?access_token="+access_token +"&fields=id%2Cname%2Curl"

    #information for username
    information_response=requests.get(information_url)
    board_response = requests.get(board_url)

    print "\n\nUser information"
    print information_response.text

    #print "\n\nBoard information"
    #print board_response.text

    user_information=json.loads(information_response.text)
    board_information=json.loads(board_response.text)

    # extracting username
    username=user_information['data']['username']
    # print username

    n=len(board_information['data'])
    print "\n" + str(n) + " board returned"

    for i in range(0,n):
        boardname = board_information['data'][i]['name']

        #print boardname

        url="https://api.pinterest.com/v1/boards/"+ username +"/"+boardname+"/pins/?access_token="+ access_token +"&fields=id%2Clink%2Cnote%2Curl%2Cboard"
        get_pins=requests.get(url)

        pins=json.loads(get_pins.text)
        print "\nPins on Board:" + boardname
        print "\n" + json.dumps(pins, indent=4)

login()