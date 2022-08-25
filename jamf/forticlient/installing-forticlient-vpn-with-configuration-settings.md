# Installing FortiClient VPN with configuration settings

There was a tool called the FortiClient Configurator used to configure a FortiClient application with the settings you defined.
As of FortiClient version 6.0.10 this Configurator has been deprecated and doesn't run unless the version of the Configurator matches the version of the supplied FortiClient application.
A new EMS product was created to replace the configuration piece.

What does remain however is the configurator postinstall function `custom_fct()` in the FortiClient VPN installer for 7.0.6.0208.

You can supply a fctdata folder alongside the installer pkg and the installer will use your conf file to configure FortiClient.

But wait how do you get the FortiClient pkg installer? You know the proper offline installer.
Its actually easy but slow:

## Download Offline Installer

1. Uninstall FortiClient
2. Download the latest FortiClient VPN Installer for macOS from https://www.fortinet.com/support/product-downloads
3. Open the DMG, go to the `Contents/MacOS` folder![image](https://user-images.githubusercontent.com/22709115/186687471-f21482e8-01b6-4f1b-b8ed-564bc79d2564.png)
4. Start a new terminal and type sudo and then drag the binary `FortiClientInstaller` into the same terminal window and press enter![image](https://user-images.githubusercontent.com/22709115/186687828-09feb703-522c-4d29-be0e-70651555403a.png)

5. Once downloaded you will see output like ```20220317 12:30:20.515 [update:INFO] fcn_upgrade:562 Download FortiClient Connect successfully. Copy it to /var/folders/zz/zyxvpxvq6csfxvn_n0000000000000/T/fctupdate/FortiClient.dmg```
6. Browse to the folder in the above message ( it will be different for you )
7. Open the DMG and voila you have the Install.pkg for the offline installer


## Add Configuration alongside the installer

1. Download the attached folder `fctdata` from this repo
2. Modify the custom.conf with the settings you require, [xml reference here](https://docs.fortinet.com/document/forticlient/7.0.2/xml-reference-guide/858086/ssl-vpn). You can also configure FortiClient VPN manually then export the configuration file and replace custom.conf.

## Testing the installer package
1. Drag the `Install.pkg` from the offline installer dmg to any empty folder
2. Drag the `fctdata` folder to the same folder
3. Run the `Install.pkg` and give PPPC permissions to the fodler when asked 
4. Check the client applicaiton has the settings you need

## Distributing the package
1. Zip up the `Install.pkg` and `fctdata` folder together
2. Add to your mdm eg for Jamf Pro just use the install package payload in a policy
3. Profit  
  
  ![image](https://user-images.githubusercontent.com/22709115/186691227-701c68be-5723-4770-ab9b-7b95365b6cd2.png)
  ![image](https://user-images.githubusercontent.com/22709115/186692943-8a8d4511-0f33-48b2-b99e-4cad91cbf759.png)
