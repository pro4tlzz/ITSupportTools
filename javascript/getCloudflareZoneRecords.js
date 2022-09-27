(async function () {
    const zoneId = getZoneId();
    if (zoneId) {
        const atok = await getToken();    
        const records = await getZoneRecords(atok, zoneId);
        console.table(records);
    } else {
        console.log('No zone id provided');
    }

    function getZoneId() {
        var zoneId = document.querySelector('pre')?.innerHTML;
        if (!zoneId) {
            zoneId = prompt('Please enter zone id:');
        }
        return zoneId;
    }    
        
    async function getToken() {
        const url = '/api/v4/system/bootstrap';
        const r = await fetch(url);
        const res = await r.json();
        const token = res.result.data.atok;
        return token;
    }

    async function getZoneRecords(atok, zoneId) {
        const url = '/api/v4/zones/' + zoneId + '/dns_records?per_page=50';
        const headers = {
            'x-atok': atok
        };
        const r = await fetch(url, {headers});
        const res = await r.json();
        const records = res.result;
        return records;
    }
})();
