# Architecting Cloud-Native Serverless Solutions

<a href="https://www.packtpub.com/product/architecting-cloud-native-serverless-solutions/9781803230085"><img src="https://m.media-amazon.com/images/I/51p95OQnhOL.jpg" alt="Book Name" height="256px" align="right"></a>

This is the code repository for [Architecting Cloud-Native Serverless Solutions](https://www.packtpub.com/product/architecting-cloud-native-serverless-solutions/9781803230085), published by Packt.

**Design, build, and operate serverless solutions on cloud and open source platforms**

## What is this book about?
Serverless computing has emerged as a mainstream paradigm in both cloud and on-premises computing, with AWS Lambda playing a pivotal role in shaping the Function-as-a-Service (FaaS) landscape. However, with the explosion of serverless technologies and vendors, it has become increasingly challenging to comprehend the foundational services and their offerings.
Architecting Cloud Native Serverless Solutions lays a strong foundation for understanding the serverless landscape and technologies in a vendor-agnostic manner. You'll learn how to select the appropriate cloud vendors and technologies based on your specific needs. In addition, you'll dive deep into the serverless services across AWS, GCP, Azure, and Cloudflare followed by open source serverless tools such as Knative, OpenFaaS, and OpenWhisk, along with examples. You'll explore serverless solutions on Kubernetes that can be deployed on both cloud-hosted clusters and on-premises environments, with real-world use cases.

This book covers the following exciting features: 
* Understand the serverless landscape and its potential
* Build serverless solutions across AWS, Azure, and GCP
* Develop and run serverless applications on Kubernetes
* Implement open source FaaS with Knative, OpenFaaS, and OpenWhisk
* Modernize web architecture with Cloudflare Serverless
* Discover popular serverless frameworks and DevOps for serverless

If you feel this book is for you, get your [copy](https://www.amazon.com/Architecting-Cloud-Native-Serverless-Solutions-ebook/dp/B0BYNX4447) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, Chapter10.

The code will look like the following:
```
[cloudshell-user@ip-10-4-174-161 firstLambda]$ touch lambda_function.py
[cloudshell-user@ip-10-4-174-161 firstLambda]$ cat lambda_function.py
import json

def lambda_handler(event, context):
   sum = event['first'] + event['second']
   return json.dumps({"sum": sum})
   
[cloudshell-user@ip-10-4-174-161 firstLambda]$ zip first_lambda.zip lambda_function.py
```

**Following is what you need for this book:**
This book is for DevOps, platform, cloud, site reliability engineers, or application developers looking to build serverless solutions. It’s a valuable reference for solution architects trying to modernize a legacy application or working on a greenfield project. It’s also helpful for anyone trying to solve business or operational problems without wanting to manage complicated technology infrastructure using serverless technologies. A basic understanding of cloud computing and some familiarity with at least one cloud vendor, Python programming language, and working with CLI will be helpful when reading this book.

With the following software and hardware list you can run all code files present in the book (Chapter 1-11).

### Software and Hardware List

| Chapter  | Software required                                                | OS required                        |
| -------- | -----------------------------------------------------------------| -----------------------------------|
| 1-11     | AWS, GCP, Azure, Cloudflare                                      | Windows, Mac OS X, and Linux (Any) |


We also provide a PDF file that has color images of the screenshots/diagrams used in this book. [Click here to download it](https://packt.link/2fHDU).

### Related products <Other books you may enjoy>
* Go for DevOps [[Packt]](https://www.packtpub.com/product/go-for-devops/9781801818896) [[Amazon]](https://www.amazon.com/Go-DevOps-language-Kubernetes-Terraform/dp/1801818894)

* Azure Containers Explained [[Packt]](https://www.packtpub.com/product/azure-containers-explained/9781803231051) [[Amazon]](https://www.amazon.in/Azure-Containers-Explained-technologies-application-ebook/dp/B0BJ7HTF9Z)

## Get to Know the Author
**Safeer CM**
He is a technology generalist with more than 16 years of experience in site reliability engineering, DevOps, infrastructure, and platform engineering. A site reliability engineer by trade, Safeer has managed large-scale production infrastructures at internet giants like Yahoo and LinkedIn and is currently working at Flipkart. He has experience in cloud management and consulting for budding and established startups as a cloud architect. He is an ambassador of the Continuous Delivery Foundation and contributes to the CD and DevOps communities. As a technology speaker, blogger and meetup organizer, Safeer enjoys mentoring new technology talents, especially in the fields of SRE and DevOps.
