(async function() {

    var zoneId = prompt("Please enter zone id:");
    if (zoneId == "") {
        alert("No value provided");
        return;
    }
    
    var headers = {
        "Accept": "*/*",
        "sec-fetch-dest": "document" ,
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-cross-site-security": "dash"    
    }

    const atok = await get_Token();    
    const records = await get_Zone_Records(atok,zoneId);
    console.log(records);
        
    async function get_Token() {
        
        const url = "https://dash.cloudflare.com/api/v4/system/bootstrap"
        const r = await fetch(url, {headers, method: 'get', credentials: 'include'});
        const result = await r.json();
        const token = result.result.data.atok;
        
        return token
    }

    async function get_Zone_Records(atok,zoneId) {

        const url = "https://dash.cloudflare.com/api/v4/zones/" + zoneId + "/dns_records?per_page=50";
        headers['x-atok'] = atok;
        headers['sec-fetch-dest'] = 'empty';
        headers['sec-fetch-mode'] = 'cors';
        const r = await fetch(url, {headers, method: 'get', credentials: 'include'});
        const result = await r.json();
        
        return result
    }
}
)();