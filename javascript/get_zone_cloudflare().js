async function get_zone() {
	const domain = window.prompt("domain please","");
    url = "https://api.cloudflare.com/client/v4/zones?name=" + domain
	const token = window.prompt("token please","");
	const email = window.prompt("email please","");
    headers = {
        "Accept": "application/json" ,
        "X-Auth-Key": '' + token,
		"X-Auth-Email": '' + email,
		"Content-Type": "application/json"
	}
	response = await fetch(url, {headers, method: 'get'})
	api_response = await response.json()
	console.log(api_response)
}