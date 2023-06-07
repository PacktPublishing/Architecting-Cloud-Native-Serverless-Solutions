# GeoIP middleman API

For this chapter’s project we are going to build a GeoIP API.  GeoIP services provide location information about a particular IP, usually the amount of information you receive varies from provider to provider.  Most of them provide a minimum of longitude and latitude, country and city where the IP is located.   GeoIP data is not always fully accurate, but it can always provide a reasonable location information.  A lot of mobile and web applications use GeoIP services to know the location of their customers, inorder to personalize the experience or show them a location specific web page or use it for legal or auditing purposes.

There are a lot of GeoIP service providers, some provide it as REST APIs while some others provide downloadable databases and SDKs alon with rolling updates. So why do we need a new GeoAPI of our own? The APIs and details of data provided vary from provider to provider. Besides the request limits on how many queries you can make to these endpoints are limited, on free as well as most paid services.  So our idea is to create a middleman API that provides a uniform GeoIP service to our applications/clients while we manage our access to the provider - including the limits and authentication mechanisms behind the scenes.  Besides you can also add a caching layer that will reduce the load on the origin API servers.  If you want to extent this service further, you can also add multiple providers in the API and balance the requests between them.

For this exercise we are going to use the Maxmind GeoLite2 API.  Maxmind is top geolocation provider - they offer both APIs and offline download of databases. Their free version of geoip is not as accurate as the paid one, but for our demonstration this will do just fine.  To start with you need to create a free account with them and then create a license key that will be needed to authenticate with their API endpoint.  More details on maxmind free service can be found at the below links:

https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
https://blog.maxmind.com/2020/12/geolite2-web-service-free-ip-geolocation-api

## Implementation

We will create a simple API endpoint that will take an IP address as the argument and return its latitude and longitude and country.  We will implement authentication for ourAPI using a simple API key ( stored in KV ) and implement some basic caching mechanism.

The API keys will be added to a KV namespace using wrangler ( since building an API key management platform is outside the scope of this project ).   We will also need an KV namespace to store the API creadentils we will use to call the Maxmind API.  For caching we could use either KV or the Cloudflare cache.  Since we looked at caching using KV in the coinbase example, we will use Cloudflare cache in this project.  Please note that unlike KV, Cloudflare cache is not global and is local the DC through with the web request came through. 


## Setting up project and KV namespaces

```
# wrangler generate geoip
# cd geoip
```

We will be creating two namespaces, one used for testint with "wangler dev" and another one for production.  This is the recommended way in which to use a namespace so that you dont corrupt your production namespace during a testing with the dev version

```
~/geoip# wrangler kv:namespace create "geo_apikeys" --preview
Creating namespace with title "geoip-geo_apikeys_preview"
Success!
Add the following to your configuration file:
kv_namespaces = [
	 { binding = "geo_apikeys", preview_id = "a4f6c9495a1647acba033980b686b49c" }
]
root@serverless101:~/geoip# wrangler kv:namespace create "geo_apikeys"
Creating namespace with title "geoip-geo_apikeys"
Success!
Add the following to your configuration file:
kv_namespaces = [
	 { binding = "geo_apikeys", id = "0d472dc3cbf64353806f447db0968cc2" }
]

```

Add both id and preview_id for the binding in the same entry in wrangler.toml as shown elow:

```
root@serverless101:~/geoip# toml get --toml-path wrangler.toml  kv_namespaces
[{'binding': 'geo_apikeys', 'id': '0d472dc3cbf64353806f447db0968cc2', 'preview_id': 'a4f6c9495a1647acba033980b686b49c'}]
```

Now let us generate a simplae API key and add it to the KV ( both preview and prod )


```
# npm install rand-token -S
# node -e 'let randtoken = require("rand-token");let token=randtoken.generate(16);console.log(token)'
rgKYA3xWbtfGv4sw

root@serverless101:~/geoip# wrangler kv:key put rgKYA3xWbtfGv4sw1 -b geo_apikeys --preview
Success

root@serverless101:~/geoip# wrangler kv:key put rgKYA3xWbtfGv4sw 1 -b geo_apikeys
Success
```

Now let us add the Maxmind API account and key as secrets - both are required to run basic auth against the API

```
root@serverless101:~/geoip# wrangler secret put MAXMIND_API_ACCOUNT
Enter the secret text you'd like assigned to the variable MAXMIND_API_ACCOUNT on the script named geoip:
668888
Creating the secret for script name geoip
Success! Uploaded secret MAXMIND_API_ACCOUNT.
root@serverless101:~/geoip# wrangler secret put MAXMIND_API_KEY
Enter the secret text you'd like assigned to the variable MAXMIND_API_KEY on the script named geoip:
hEuPDocBDEq8UKeM
Creating the secret for script name geoip
Success! Uploaded secret MAXMIND_API_KEY.

```

You should declare your secrets by adding a section like below to your wrangler.toml file

```
#[secrets]
#MAXMIND_API_KEY
#MAXMIND_API_ACCOUNT
```

Once this is done, you can copy over the index.js file from this repo to replace the index file inside the worker directory.

```
root@serverless101:~/geoip# git@github.com:PacktPublishing/Architecting-Cloud-Native-Serverless-Solutions.git /tmp/servereless
root@serverless101:~/geoip# cp /tmp/serverless/chapter-6/geoip/index.js index.js
```

You can test locally by running 

```
root@serverless101:~/geoip$ wrangler dev -i 0.0.0.0

## Test from local

$curl -s -H "X-API-Key: rgKYA3xWbtfGv4sw" "https://{IP_OF_THE_DEV_SERVER_OR_LOCALHOST}}/8.8.8.8"|jq .
{
  "country": "US",
  "latitude": 37.751,
  "longitude": -97.822
}
```

Once this is confirmed to be working, deploy to cloudflare

```
root@serverless101:~/geoip# wrangler publish
Basic JavaScript project found. Skipping unnecessary build!
Successfully published your script to
 https://geoip.safeer.workers.dev
```

Now test with same API Key against this domain

```
$ curl -s -H "X-API-Key: rgKYA3xWbtfGv4sw" "https://geoip.safeer.workers.dev/8.8.8.8"|jq .
{
  "country": "US",
  "latitude": 37.751,
  "longitude": -97.822
}
```

Your worker project is up and running.  Two things to note:

1. The Cloudflare cache manipulation is not done in this code since it requires a custom domain hosted with cloudflare.  It wont work with workers.dev domain.
2.  When storing API keys, the best practice is to store only a one-way hash of the API key and not the API key directly.  This way if your KV is compromised, the PAI Keys wont cant be misused.

We will fix this and add a few more feature in the next iteration of this project.



