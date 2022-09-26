async function get_zone_records() {
    var pathArray = window.location.pathname.split('/');
    var zoneId = pathArray[1];
    console.log(zoneId);
    const url = "https://dash.cloudflare.com/api/v4/zones/" + zoneId + "/dns_records?per_page=50";
    console.log(url);
    headers = {
        "Accept": "*/*",
        "sec-fetch-dest": "document" ,
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-cross-site-security": "dash",
        "x-atok": "this is required for auth, seems to be one time"
	}
    records = await fetch(url, {headers, method: 'get', credentials: 'include'});
    result = await records.json();
    console.log(result);
}
get_zone_records()