# Javascript Web Browser Scripts

## Why JavaScript?
JavaScript can run natively in Chromium based browsers and with Javascript you can do things that you can code in other languages such as Python.
Using JavaScript eliminates the barrier of having to learn how to use an API client. One of the things I've enjoyed learning is how GUIs authorise and authenticate requests to APIs which then bring you back data on a fancy HTML web page.
Another benefit of JavaScript is you can use your learning and apply that to other languages.

## Special thank you
Before I go any further I'd like to give a big shoutout to [Gabriel Sroka](https://github.com/gabrielsroka/) who you may know as developer of [Rockstar](https://chrome.google.com/webstore/detail/rockstar/chjepkekmhealpjipcggnfepkkfeimbd) for Okta.
Gabriel has taught me some key things about JavaScript and helped refactor my 'midnight' code. Also you'll notice I reuse certain functions from Rockstar and from [okta_api](https://github.com/gabrielsroka/okta_api/blob/master/okta_api.py) as well.

### Requirements and usage

#### Requirements

I've only tested these scripts on Brave, Microsoft Edge and Google Chrome which are Chromium based browsers.

#### Usage

How to use these scripts:

1. Copy the contents of a script from this folder into your clipboard.
2. Launch the Chrome Developer tools by pressing ctrl + shift + i or right click the page and press inspect.
3. Browse to the sources tab and then to snippets![image](https://user-images.githubusercontent.com/22709115/193648888-e002c4a0-163f-41d9-94f3-759398741cf5.png)
4. Click new snippet and give the snippet a name.
5. Paste the code from your clipboard into the code editor, then press ctrl + s to save the script.
6. Follow the specific steps below for each script.

Note: Right click the name of the script to run it.


#### Okta

##### Clone application signing keys to another application
You might have a use case for having 2 or more Saml applications in Okta which need to use the same signing certificate. The Okta Apps API allows you to copy an application signing key to another app.
Here is a script which can clone the signing certificate from an application and paste it to another application.

##### Usage

Primary app is the application to copy the siging key from.
Target app is the application to paste the signing key from the primary app.
My example is with Google Workspace.

In my example:

Primary app has the signing key ```G92BQvTQ-SBxzS3MgBsrG5O4NwEWHOvNyQNdIJs80nI``` ![image](https://user-images.githubusercontent.com/22709115/193650773-206d5607-00b5-45cf-826e-cbefd3b73931.png)
Target app has the signing key ```MbfFdXiogWGXH3GoyyguLs2k34zDJbQIXBIOwRwTKfk``` ![image](https://user-images.githubusercontent.com/22709115/193650873-fe280d0f-5ba2-431a-93ec-d58972e00c8b.png)

</br>

1. Follow Usage above to install the script.
2. Create the target Saml app in Okta and configure the settings for the application (Only configure the app in Okta, not the Service Provider).
3. Browse to the primary application in Okta Admin from where you want to clone the signing certificate.
4. Right click the script to run it.![image](https://user-images.githubusercontent.com/22709115/193651211-fa872a81-eb86-49a0-9578-aa174c700b56.png)
5. Enter the id of the Target App when prompted.
6. Profit.![image](https://user-images.githubusercontent.com/22709115/193651514-81f5e9ba-33ce-43b2-919c-ff9a1df1c48e.png)
7. See how the signing key is now the same as the Primary App. ![image](https://user-images.githubusercontent.com/22709115/193651651-1114da4b-2256-42f9-8772-008c23fd3ade.png)

#### Cloudflare
