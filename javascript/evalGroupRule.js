(async function () {

    var headers = {
        'accept': 'application/json',
        'content-type' : 'application/json'
    }
    
    const ruleName = await getRuleName();
    const rule = await getRule(ruleName);
    const userId = await getUserId();
    await evalGroupRule(rule,userId);
    
    async function getRuleName() {

        const ruleName = prompt('Please enter rule name');
    
        if (!ruleName) {
            const ruleName = prompt('Please enter rule name');
        }
    
        return ruleName;
        
    }

    async function getRule(ruleName) {

        const url = '/api/v1/groups/rules?search=' + ruleName + '&limit=1';
        const r = await fetch(url);
        
        if (r.ok = true) {

            const rules = await r.json();
            const rule = rules[0];
            console.log(rule);
            return rule;   
            
        } else {
            alert("Couldn't find matching rule");
            return false;
        }
    }

    async function getUserId() {
        
        const userId = prompt('Please enter user Id');
    
        if (!userId) {
            const userId = prompt('Please enter user Id');
        }

        console.log(userId);
    
        return userId;
    }

    async function evalGroupRule(rule,userId) {

        const ruleValue = rule.conditions.expression.value;

        const url = '/api/v1/internal/expression/eval';

        headers['X-Okta-XsrfToken'] =  document.querySelector('#_xsrfToken').innerText;
        
        const body = JSON.stringify([{
            
            "type":"urn:okta:expression:1.0",
            "value": ruleValue,
            "targets":{"user":userId},
            "operation":"CONDITION"
        
        }]);
        console.log(body);
        
        const r = await fetch(url, {method: 'post', body, headers});
        const eval = await r.json();
        let evalResult = eval[0].result;
        console.log(evalResult);

        if (evalResult = "TRUE") {
            alert('User Matched rule');
            return true;
        }
       /// this branch below doesn't work
        else {
                alert('User didn\'\t match rule');
                return false;
            }

        
    }
    
})();