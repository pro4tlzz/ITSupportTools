def generate_Google_Access_Token(client_Id,client_Secret,refresh_Token):

    try:

        url = "https://www.googleapis.com/oauth2/v4/token"

        headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        }

        body = json.dumps({
        "client_id": client_Id,
        "client_secret": client_Secret,
        "refresh_token": refresh_Token,
        "grant_type": "refresh_token"
        })

        response = requests.request(
        "POST",
        url,
        headers=headers,
        data=body
        )

        apiResponse = response.json()
        access_Token = apiResponse["access_token"]
        return access_Token

    except:

        print("\033[1m"+"Issue Occured with generating Google Vault Access Token"+"\033[0m")
        sys.exit(1)


def get_Export_Status(matterId,headers):

    try:

        url = "https://vault.googleapis.com/v1/matters/"+matterId+"/exports/"
        
        response = requests.request(
        "GET",
        url,
        headers=headers,
        )

        apiResponse=response.json()
        status=apiResponse["exports"][0]["status"]

        while status == "IN_PROGRESS":

                response = requests.request(
                "GET",
                url,
                headers=headers,
                )

                apiResponse=response.json()
                status=apiResponse["exports"][0]["status"]
                print("Export is not completed yet. Going to sleep for 30 seconds, then I will check the export status again")
                time.sleep(30)

        if status == "COMPLETED":
            cloudStorageSink=apiResponse["exports"][0]["cloudStorageSink"]["files"]
        return cloudStorageSink

    except:

        print("\033[1m"+"Issue Occured with status of Google Vault Export"+"\033[0m")
        sys.exit(1)

def download_Export(objectName,bucketName,size,md5Hash,header,user):

    try:

        encoded=urllib.parse.quote(objectName,safe='')
        download_url="https://storage.googleapis.com/storage/v1/b/"+bucketName+"/o/"+encoded+"?alt=media"
        directory=user
        parent_dir="downloads"
        path = os.path.join(parent_dir, directory)
        os.makedirs(path, exist_ok=True)
        last = objectName.split("/")[-1]
        print(last)
        fileName=(path+"/"+last)

        with requests.get(download_url, stream=True,headers=headers) as r:
                PreparedResponse=requests.get
                with open(fileName, 'wb') as f:
                    shutil.copyfileobj(r.raw, f, length=16*1024*1024)

        return fileName

    except:

        print("\033[1m"+"Issue Occured with downloading Google Vault Export"+"\033[0m")
        sys.exit(1)

access_Token=generate_Google_Access_Token(client_Id,client_Secret,refresh_Token)
headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization": "Bearer " + access_Token
}
exportList=get_Export_Status("matterId",headers)

count=0x
for each in exportList:
    count+=1
    objectName=each["objectName"]
    bucketName=each["bucketName"]
    size=each["size"]
    md5Hash=each["md5Hash"]
    #print(objectName,bucketName,size,md5Hash)
    download_Export(objectName,bucketName,size,md5Hash,header,"user@domain.com")
