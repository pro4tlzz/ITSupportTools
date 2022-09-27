(async function() {
    
    var headers = {
        
        "Accept": "application/json",
        "x-cross-site-security": "dash"    
        
    }

    zoneId = await getZoneId();
    const atok = await getToken();    
    const records = await getZoneRecords(atok,zoneId);
    console.table(records);

    async function getZoneId() {
        
        try {
        
            const zoneId = document.querySelector('pre').innerHTML;
            return zoneId;
        
        }
        
        catch(err) {
        
            const zoneId = prompt("Please enter zone id:");
            if (zoneId == "") {
                alert("No value provided");
                return;
            }
            
            return zoneId;
        
        }
    }    
        
    async function getToken() {
        
        const url = "https://dash.cloudflare.com/api/v4/system/bootstrap";
        const r = await fetch(url, {headers, method: 'get'});
        const result = await r.json();
        const token = result.result.data.atok;
        return token;
        
    }

    async function getZoneRecords(atok,zoneId) {

        const url = "https://dash.cloudflare.com/api/v4/zones/" + zoneId + "/dns_records?per_page=50";
        headers['x-atok'] = atok;
        const r = await fetch(url, {headers, method: 'get'});
        const result = await r.json();
        const records = result.result;
        return records;
        
    }
}
)();