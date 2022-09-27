(async function() {

    const zoneId = await getZoneId();
    
    if (zoneId != false) {
        const atok = await getToken();    
        const records = await getZoneRecords(atok,zoneId);
        console.table(records);
    }

    function getZoneId() {

        const zoneId = document.querySelector('pre')?.innerHTML;

        if (zoneId) { return zoneId; }
            
        else {
            const zoneId = prompt("Please enter zone id:");
            if (zoneId) {return zoneId;}
            else {
                alert("No value provided");
                return false;
                 }
        }
        
    }    
        
    async function getToken() {
        
        const url = "https://dash.cloudflare.com/api/v4/system/bootstrap";
        const headers = {
            'x-cross-site-security': 'dash'
        }
        headers['x-cross-site-security'] = 'dash';
        const r = await fetch(url, {headers, method: 'get'});
        const result = await r.json();
        const token = result.result.data.atok;
        return token;
        
    }

    async function getZoneRecords(atok,zoneId) {

        const url = "/api/v4/zones/" + zoneId + "/dns_records?per_page=50";
        const headers = {
            'x-atok': atok
        }
        const r = await fetch(url, {headers, method: 'get'});
        const result = await r.json();
        const records = result.result;
        return records;
        
    }
}
)();