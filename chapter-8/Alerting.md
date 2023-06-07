The laerting function is very simple. This function will be part of a sequnce, where it will recieve a cloudnt record as parameter from the previous action in the squence.  All this function has to do it look into the cloudnt record/document, check if it breaches a certian threshold and alert on it.

The code is available at [code/alerting/__main__.py](code/alerting/__main__.py).  Since you ahve already checkout this repo, switch to the directory `chapter-8` and run the following commands

```
ibmcloud fn action create alerting code/alerting/__main__.py --kind python:3.9 --param threshold 50
```

This will create the alerting cloud function and pass the threshold of 50 as the parameter.  

Now that we have completed all the subtaks, lets go and start connecting the moving pieces.

