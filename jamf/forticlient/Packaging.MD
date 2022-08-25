# Installing FortiClient VPN with configuration settings

There was a tool called the FortiClient Configurator used to configure a FortiClient application with the settings you defined.
As of FortiClient version 6.0.10 this Configurator has been deprecated and doesn't run unless the version of the Configurator matches the version of the supplied FortiClient application.

What does remain however is the configurator postinstall function `custom_fct()` in the FortiClient VPN installer for 7.0.6.0208.

You can supply a fctdata folder alongside the installer pkg and the installer will use your conf file to configure FortiClient.

But wait how do you get the FortiClient pkg installer? You know the proper offline installer.
Its actually easy but slow:
