async function get_Vault_Export(client_id,client_secret,refresh_token) {
    url = 'https://www.googleapis.com/oauth2/v4/token'
    headers = {
        'accept': 'application/json',
        'content-type': 'applicaton/json',
    }
	data = {
	    'client_id': '' + client_id,
        'client_secret': '' + client_secret,
        'refresh_token': '' + refresh_token,
        'grant_type': 'refresh_token'
        }
	const body = JSON.stringify(data);
	response = await fetch(url, {headers, body, method: 'post'})
    apiResponse = await response.json()
	access_token = apiResponse.access_token
	
	const pathname = window.location.pathname.split("/");
	const matterId = pathname[pathname.length - 2];
	console.log(matterId)
	
	url = "https://vault.googleapis.com/v1/matters/"+matterId+"/exports/"
	
	console.log(url)
	
	headers = {
        'accept': 'application/json',
        'content-type': 'applicaton/json',
		'authorization': 'Bearer ' + access_token
    }
	
	response = await fetch(url, {headers, method: 'get'})
	apiResponse = await response.json()
	console.log(apiResponse)
	
	}
	