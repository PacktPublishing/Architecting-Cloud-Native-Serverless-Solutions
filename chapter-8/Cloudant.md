# Creating an IBM Cloudnat Database 

Inorder to make an IBM Cloudant database, you first need to create a resource/instance of Cloudant in you IBM Cloud account.  After that you can launch the console of this instance from the cloud UI and create a databases.  You also need to create and get the credentials for this instance to access the DBs from our code.  Following link details out how to create an instanec of cloudant and retrieving its credentails, since it is a straight forward process you can follow the link and get it done.  It is preferred to launch this instance in the same region/location as our WAtson instance, in this case it is London.

[Getting started with IBM Cloudant ](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-getting-started-with-cloudant)

Once this section is completed and you have save the credentials for later use, launch the cloudant instance page by goign into https://cloud.ibm.com/resources and then selectign the cloudant instance and clicking on it ( you might have to search for the resource if there are too many).

On the cloudant page you will see the details of your instance and also a blue button to "Launch Dashboard".  Click on that and it will take you to a cloudnat specific URL from where you can create and manage databases. 

Create a database by the name `serverless-db1`

We will use this database in the subsequent sections.