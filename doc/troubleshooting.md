Troubleshooting
===============

What is the default port? How do I change it?
---------------------------------------------

The default port is 5000 and you can change it by tweaking the file /etc/nginx/sites-available/ble2json.conf.
Remember to restart nginx afterwards with `sudo systemctl restart nginx.service`.


I get "502 Bad Gateway" on every request
----------------------------------------

This means nginx cannot reach the Python app because the latter has crashed 
for an unknown reason, or was never started in the first place. This is most likely due 
to missing package files or incorrect file permissions, which can usually be fixed by 
removing and reinstalling the package. You should run `sudo systemctl status ble2json.service` 
to see what the app is doing, and whether there are any useful error messages included in the output.


I get status 500 and a "Config Error" although I already fixed the config file
------------------------------------------------------------------------------

You should always restart the app with `sudo systemctl restart ble2json.service` after
editing the config file.
