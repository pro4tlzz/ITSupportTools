import requests
import json
import sys

credentials_User=sys.argv[1]
credentials_Password=sys.argv[2]
email=sys.argv[3]

def auth_api(login_User,login_Password,):

    try:

        gooddata_user=login_User
        gooddata_password=login_Password
        body = json.dumps({
        "postUserLogin":{
            "login": gooddata_user,
            "password": gooddata_password,
            "remember":1,
            "verify_level":0
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

        url="https://yourdomain.yourdomain.com/gdc/account/login"

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=body
        )
        sst=response.headers.get('Set-Cookie')
        return sst

    except:
        print("\033[1m"+"Issue Occured with authenticating to GoodData API"+"\033[0m")
        sys.exit(1)

def query_api(cookie,email):

    try:

        url="https://yourdomain.yourdomain.com/gdc/account/domains/yourdomain/users?login="+email
        
        body={}

        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': cookie
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            data=body
        )

        jsonContent=json.loads(response.text)
        accountMain=jsonContent["accountSettings"]["items"][0]
        accountLink=accountMain["accountSetting"]["links"]["self"]
        profilehash=accountLink.rsplit('/')[4]
        print("ProfileHash is "+profilehash)
        return profilehash

    except:
        print("\033[1m"+"Issue Occured with retrieving account information from API or authentication is invalid"+"\033[0m")
        sys.exit(1)

def get_user(cookie,profilehash):

    try:

        url="https://yourdomain.yourdomain.com/gdc/account/profile/"+profilehash

        body={}

        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': cookie
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            data=body
        )

        jsonContent=json.loads(response.text)
        firstname=jsonContent["accountSetting"]["firstName"]
        lastname=jsonContent["accountSetting"]["lastName"]
        print("User firstname and lastname are "+firstname,lastname)
        return firstname,lastname
    except:
        print("\033[1m"+"Issue Occured with retrieving account information from API"+"\033[0m")
        sys.exit(1)

def update_user(cookie,profilehash,userinfo):

    try:

        url="https://yourdomain.yourdomain.com/gdc/account/profile/"+profilehash

        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': cookie
        }
        firstName=userinfo[0]
        print("First Name "+firstName)
        lastName=userinfo[1]
        print("Last Name "+lastName)

        body = json.dumps({
        "accountSetting" : {
            "firstName": firstName,
            "lastName": lastName,
            "authenticationModes" : [
                "SSO"
            ],
            "ssoProvider" : "yourdomain.com"
        }
        })

        response = requests.request(
            "PUT",
            url,
            headers=headers,
            data=body
        )

        print("URL PUT to "+url)
        print("JSON to PUT "+body)
        jsonContent=json.loads(response.text)
        print(jsonContent)

    except:
        print("\033[1m"+"Issue Occured with user account in GoodData API"+"\033[0m")
        sys.exit(1)

cookie=auth_api(credentials_User,credentials_Password)
profilehash=query_api(cookie,email)
userinfo=get_user(cookie,profilehash)
update_user(cookie,profilehash,userinfo)