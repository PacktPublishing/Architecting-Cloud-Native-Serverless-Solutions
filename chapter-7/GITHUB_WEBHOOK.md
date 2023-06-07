# Create github repo and webhook

This can be done either from the github web or using the gh CLI.  I am going to use the gh CLI.


```
safeer@serverless102:~$ gh repo create openshift-webhook-test --private
✓ Created repository safeercm/openshift-webhook-test on GitHub

safeer@serverless102:~$ gh repo clone safeercm/openshift-webhook-test
Cloning into 'openshift-webhook-test'...
warning: You appear to have cloned an empty repository.

```

The next step need to be done after you setup the webhook endpoint in openshift.  Create that and come back with the URL of the application to setup this.  For demonstration am using a dummy link.

```
safeer@serverless102:~$ echo '{ "name": "web", "active": true, "events": [ "push" ], "config": { "url": "https://os-pyhttptest-safeercm-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com", "content_type": "json" } }' | gh api /repos/safeercm/openshift-webhook-test/hooks -H "Accept: application/vnd.github.v3+json" --input  -
{
  "type": "Repository",
  "id": 354605005,
  "name": "web",
  "active": true,
  "events": [
    "push"
  ],
  "config": {
    "content_type": "json",
    "url": "https://os-pyhttptest-safeercm-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com",
    "insecure_ssl": "0"
  },
  "updated_at": "2022-04-22T15:27:09Z",
  "created_at": "2022-04-22T15:27:09Z",
  "url": "https://api.github.com/repos/safeercm/openshift-webhook-test/hooks/354605005",
  "test_url": "https://api.github.com/repos/safeercm/openshift-webhook-test/hooks/354605005/test",
  "ping_url": "https://api.github.com/repos/safeercm/openshift-webhook-test/hooks/354605005/pings",
  "deliveries_url": "https://api.github.com/repos/safeercm/openshift-webhook-test/hooks/354605005/deliveries",
  "last_response": {
    "code": null,
    "status": "unused",
    "message": null
  }
}

```

That is it, you are all set to use the webhook.