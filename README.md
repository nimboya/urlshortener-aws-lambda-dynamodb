# Simple URL Shortener using AWS Lambda and Dynamo DB using Chalice Framework

Simply shorten a URL and get a short link from the long url

- AWS Lambda
- API Gateway
- DynamoDB
- Chalice Framework


## Setup

Create `.chalice/config.json`

```console
$ cat .chalice/config.json
{
    "stages": {
        "dev": {
        "api_gateway_stage": "api",
        "environment_variables": { "APP_TABLE_NAME": "itsshort" }
        }
    },
    "version": "2.0",
    "app_name": "itsshort"
}
```

#### Environment Variables on your local machine

```sh
export APP_TABLE_NAME=xxxxxxxxxxxxxxxxxxxx
```
