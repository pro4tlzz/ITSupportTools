(async function() {

    const headers = {
        "Accept": "*/*",
        "sec-fetch-dest": "document" ,
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-cross-site-security": "dash"    
    }

    const atok = await get_Token();
    console.log(atok)
        
    async function get_Token() {
        const url = "https://dash.cloudflare.com/api/v4/system/bootstrap"
            
        const r = await fetch(url, {headers, method: 'get', credentials: 'include'});
        const result = await r.json();
        const token = result.result.data.atok;
        return token
    }
}
)();