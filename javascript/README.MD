# JavaScript Web Browser Scripts / Bookmarklets

- [JavaScript Web Browser Scripts / Bookmarklets](#javascript-web-browser-scripts--bookmarklets)
  - [Why JavaScript?](#why-javascript)
  - [Special thank you](#special-thank-you)
  - [Requirements and installation](#requirements-and-installation)
    - [Requirements](#requirements)
    - [Installation](#installation)
  - [Okta](#okta)
    - [Clone application signing keys to another application](#clone-application-signing-keys-to-another-application)
      - [Usage](#usage)
    - [Evaluate a group of users against a group rule](#evaluate-a-group-of-users-against-a-group-rule)
      - [Usage](#usage-1)
  - [Cloudflare](#cloudflare)
    - [Show DNS records in the console table](#show-dns-records-in-the-console-table)
      - [Usage](#usage-2)

## Why JavaScript?
JavaScript can run natively in browsers and with JavaScript you can do things that you can code in other languages such as Python.
Using JavaScript eliminates the barrier of having to learn how to use an API client. One of the things I've enjoyed learning is how GUIs authorise and authenticate requests to APIs which then bring you back data on a fancy HTML web page.
Another benefit of JavaScript is you can use your learning and apply that to other languages.

## Special thank you
Before I go any further I'd like to give a big shoutout to [Gabriel Sroka](https://github.com/gabrielsroka/) who you may know as developer of [rockstar](https://gabrielsroka.github.io/rockstar) for Okta.
Gabriel has taught me some key things about JavaScript and helped refactor my 'midnight' code. Also you'll notice I reuse certain functions from rockstar JavaScript code and from [okta_api](https://github.com/gabrielsroka/okta_api/blob/master/okta_api.py) Python code as well. Why reinvent the wheel when good code exists?

## Requirements and installation

### Requirements

I've only tested these scripts on Brave, Microsoft Edge and Google Chrome which are Chromium based browsers, but they should work on Safari, Firefox, etc.

### Installation

How to install these scripts:

1. Copy the contents of a script from this folder into your clipboard.
2. Add a new bookmark, give it a nice name and copy the contents of the script to the URL box. ![image](https://user-images.githubusercontent.com/22709115/195946862-45d4ec41-7011-4951-a7ab-e859b56183c5.png)


Note: Click the new bookmark to run the script.


## Okta

### Clone application signing keys to another application
[Script](cloneSourceAppKidToTargetApp.js).

You might have a use case for having 2 or more SAML applications in Okta which need to use the same signing certificate. The Okta Apps API allows you to copy an application signing key to another app.
Here is a script which can clone the signing certificate from an application and assign it to another application.

#### Usage

Primary app is the application to copy the siging key from.
Target app is the application to paste the signing key from the primary app.
My example is with Google Workspace.

In my example:

Primary app has the signing key ```G92BQvTQ-SBxzS3MgBsrG5O4NwEWHOvNyQNdIJs80nI``` ![image](https://user-images.githubusercontent.com/22709115/193650773-206d5607-00b5-45cf-826e-cbefd3b73931.png)
Target app has the signing key ```MbfFdXiogWGXH3GoyyguLs2k34zDJbQIXBIOwRwTKfk``` ![image](https://user-images.githubusercontent.com/22709115/193650873-fe280d0f-5ba2-431a-93ec-d58972e00c8b.png)

</br>

1. Follow Installation above to install the script.
2. Create the target SAML app in Okta and configure the settings for the application (Only configure the app in Okta, not in the Service Provider).
3. Browse to the primary application in Okta Admin from where you want to clone the signing certificate.
4. Click the created bookmark to run the script.
5. Enter the id of the Target App when prompted.
6. Profit.![image](https://user-images.githubusercontent.com/22709115/193651514-81f5e9ba-33ce-43b2-919c-ff9a1df1c48e.png)
7. See how the signing key is now the same as the Primary App. ![image](https://user-images.githubusercontent.com/22709115/193651651-1114da4b-2256-42f9-8772-008c23fd3ade.png)

### Evaluate a group of users against a group rule
[Script](evalGroupRule.js).

A common thing to do when creating a group rule is to preview the rule for a specific user, what about if you want to evaluate against multiple users? Then this script is for you, ps also check out [this Python version](https://github.com/pro4tlzz/ITSupportTools/blob/main/okta/group-rules/eval-group-rules.py).

In my example:

I have a group rule with the id ```0pr6ousv8vfWcZYl05d7``` with the condition ```user.login==\"google.com\"```.
I also have an Okta group with the users I want to test the rule against.

#### Usage

1. Follow Installation above to install the script.
2. Browse to the Okta group with the users you want to test against.
3. Click the created bookmark to run the script.
4. Enter the group rule id when prompted.
5. Read through the results in the browser console, there is a neat table to read through. ![image](https://user-images.githubusercontent.com/22709115/193654630-f0f94841-9015-45bf-bf7e-3a238ed62d6b.png)

## Cloudflare

### Show DNS records in the console table
[Script](getCloudflareZoneRecords.js).

This script was more for learning as to how the Cloudflare Dashboard authenticates to the API.

#### Usage

1. Follow Installation above to install the script.
2. Browse to the Cloudflare Dashboard and then the Overview page of the domain you want to see DNS records for.
3. If you haven't browsed to your the Overview page then copy the zone id.
4. Click the created bookmark to run the script. and enter the zone id when prompted.
5. Profit and see the DNS records.![image](https://user-images.githubusercontent.com/22709115/193655473-8a62528e-bf1b-48ab-830d-74cb749f3b8a.png)
