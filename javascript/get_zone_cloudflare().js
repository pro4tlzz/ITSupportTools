async function get_zone() {
	const domain = window.prompt("domain please","");
    url = "https://api.cloudflare.com/client/v4/zones?name=" + domain;
	const token = window.prompt("token please","");
	const email = window.prompt("email please","");
    headers = {
        "Accept": "application/json" ,
        "X-Auth-Key": '' + token,
		"X-Auth-Email": '' + email,
		"Content-Type": "application/json"
	}
	response = await fetch(url, {headers, method: 'get'});
	result = await response.json();
	zone = result.result[0].id;
	console.log(zone);
}
get_zone()

// because of CORS you need to run from https://api.cloudflare.com/