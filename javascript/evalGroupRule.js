javascript:
/* /evalGroupRule# */
(async function () {

    const headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'X-Okta-XsrfToken': document.querySelector('#_xsrfToken').innerText
    };
    
    const groupId = getGroupId();
    const groupRuleId = getGroupRuleId();

    if (!groupId || !groupRuleId) return;

    const groupMembers = await getGroupMembers(groupId);
    const rule = await getGroupRule(groupRuleId);
    const tableResult = [];

    for (const member of groupMembers) {

        const eval = await evalGroupRule(rule, member, tableResult, 10);
        
        const data = {
            userId: member.id,
            username: member.profile.login,
            ruleValue: rule.conditions.expression.value,
            evalResult: eval
        };
        
        tableResult.push(data);
            
    }

    console.table(tableResult);

    /* from Rockstar https://github.com/gabrielsroka/gabrielsroka.github.io/blob/master/rockstar/rockstar.js#L774 */
    function getGroupId() {
        var path = location.pathname;
        var pathparts = path.split('/');
        if (path.match("admin/group") && (pathparts.length == 4)) {
            return pathparts[3];
        }
    }

    function getGroupRuleId() {
        
        const groupRuleId = prompt('Please enter the group rule id');
        if (groupRuleId) {
            return groupRuleId;
        } else {
            alert("No value provided");
            return false;
        }
    }
    
    /* from Gabriel Sroka https://github.com/gabrielsroka/gabrielsroka.github.io/blob/master/snippets/AppKeys.js#L40 */
    function getLinks(linkHeader) {
        var headers = linkHeader.split(", ");
        var links = {};
        for (var i = 0; i < headers.length; i++) {
            var [, url, name] = headers[i].match(/<(.*)>; rel="(.*)"/);
            links[name] = url;
        }
        return links;
    }

    /* from Gabriel Sroka https://github.com/gabrielsroka/gabrielsroka.github.io/blob/master/snippets/AppKeys.js#L31 */
    function getNextUrl(linkHeader) {
        const links = getLinks(linkHeader);
        if (links.next) {
            const nextUrl = new URL(links.next); /* links.next is an absolute URL; we need a relative URL. */
            return nextUrl.pathname + nextUrl.search;
        } else {
            return null;
        }
    }

    async function getGroupRule(groupRuleId) {

        const url = '/api/v1/groups/rules/' + groupRuleId;
        const r = await fetch(url, {headers});
        const rule = await r.json();
        return rule;

    }

    async function getGroupMembers(groupId) {

        var groupMembers = [];
        var url = '/api/v1/groups/' + groupId + '/users?limit=200';
        while (url) {
            const r = await fetch(url, {headers});
            const members = await r.json();
            groupMembers = groupMembers.concat(members);
            sleep(r, 10);
            url = getNextUrl(r.headers.get('link'));
        }
        return groupMembers;

    }

    async function evalGroupRule(rule, user, tableResult, limitRemaining) {

        const ruleValue = rule.conditions.expression.value;
        const url = '/api/v1/internal/expression/eval';        
        const body = JSON.stringify([{
            type: "urn:okta:expression:1.0",
            value: ruleValue,
            targets: {user: user.id},
            operation: "CONDITION"
        }]);
        
        const r = await fetch(url, {method: 'post', body, headers});
        const eval = await r.json();
        const result = eval[0].result;
        sleep(r, 10);
        
        return result;
    }

    async function sleep(r, limitRemaining) {

        const rateLimit = r.headers.get('x-rate-limit-limit');
        const rateLimitRemaining = r.headers.get('x-rate-limit-remaining');
        const rateLimitReset = r.headers.get('x-rate-limit-reset');
        
        var rateLimitResetUTC = new Date(0);
        rateLimitResetUTC.setUTCSeconds(rateLimitReset);
        const now = Date.now();

        /* Limit like okta_api.py https://github.com/gabrielsroka/okta_api/blob/master/okta_api.py#L148 */
        if (rateLimitRemaining < limitRemaining) {
    
            while ( rateLimitReset > now ) {
                
                console.log('Sleeping due to less than ' + limitRemaining +' requests left. Limit : '+ rateLimit + ' Remaining : ' + rateLimitRemaining + ' Reset : ' + rateLimitResetUTC);
                await new Promise(r => setTimeout(r, 2000));
                now = Date.now();
                
            }

        }

    }

}
)();
