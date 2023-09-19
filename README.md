# Tool

Tool is an Independent Sales Organization in partnership with Evolve Bank & Trust. Its main purpose is to deliver
and continuously improve merchant services to Evolve’s corporate clients. One area where merchant services can be
improved is related to ACH. Businesses in the US increasingly rely on ACH transactions for crediting vendors and
debiting customers. The ACH Network is a batch-oriented electronic funds transfer system. It is regulated by Nacha
Operating Rules which are highly complex and constantly changing. As a result businesses have to allocate additional
financial and human resources into creating NACHA compliant ACH files.

In order to more effectively retain existing customers and attract new ones Tool decided to invest into a web
platform which would exploit the opportunities created by these improvement areas. Tool web platform is meant to
solve the above-mentioned pain points for Tool clients in the following ways:

1. The platform will automate NACHA-compliant ACH files creation based on user’s input into simple web forms or
   uploading easy-to-understand CSV templates. This will not only eliminate the need for investing into NACHA compliance
   but also will reduce ACH returns by minimizing the risk of errors.
2. To prevent Users from ACH returns the platform will verify Routing numbers of Users` vendors and customers and will
   have Prenotes functionality.
3. The platform will keep the history of ACH transactions and receivers’ information which will allow businesses to have
   all ACH-related information in one place.
4. Unlike similar ACH file generation apps, Tool will be much more intuitive and user-friendly.

## Getting Started

### Project setup

```shell
$ git clone ...
$ cd pg-back/
$ virtualenv .venv -p python3.9
$ . .venv/bin/activate
$ git checkout develop
$ make install
$ make docker-up
$ make migrate
```

### Testing

Run test env:

```shell
$ make docker-testenv
```

Run tests:

```shell
$ make test
```

#### Docker

You need to have Docker installed in your development environment.

Docker image is used for both - running in production and on developers' machines as dependency (use `docker-compose`).
Here's how you can build docker image locally.

Run the build:

```shell
$ make docker-build
```

Restart containers:

```shell
$ make docker-down
$ make docker-up
```

Check Swagger docs:
[http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

Check docker logs:

```shell
$ make docker-logs
```

Log in to the bash on the service

```shell
$ make docker-bash
```
## Alembic work

Merge alembic migrations:


```shell

$ make alembic-merge-heads-local

```

Make migrations:

```shell

$ make migrations
```

Apply migrations:

```shell

$ make migrate
```

# Getting Started with Server Development

All server development is done with Python

## Environment variables

We use a **.env** file to store non-private temporary keys. If you need to keep the private key, use the **.profile**
file. Instructions below

Required environment vars for the project are:

* **POSTGRES_DB** - This is for the Postgres connection string for the admin schema. This will be in the format:
  postgresql://username:pwd@host/dbname
* **POSTGRES_USER** - This is for the Postgres connection string for the data schema. This will be in the format:
  postgresql://username:pwd@host/dbname
* **POSTGRES_PASSWORD** - This is for the Postgres connection string for the data schema. This will be in the format:
  postgresql://username:pwd@host/dbname
* **POSTGRES_PORT** - This is for the Postgres connection string for the data schema. This will be in the format:
  postgresql://username:pwd@host/dbname
* **POSTGRES_HOST** - This is for the Postgres connection string for the data schema. This will be in the format:
  postgresql://username:pwd@host/dbname
* **LOCALSTACK_HOST** - HOST for localstack
* **AWS_ACCESS_KEY_ID** This is for local stack. Must be empty
* **AWS_SECRET_ACCESS_KEY** - This is for local stack. Must be empty

## Handling Passwords and Secret Keys using Environment Variables

To set password or secret keys in environment variable on Linux(and Mac) you need to modify
**.profile** file that is in your home directory. You need to open the terminal and cd to the home directory.

```shell
$ cd
```

Now, open the .profile file in any text editor of your choice.

```shell
$ vim .profile
```

We need to add our environment variable in this file. For that add following content at the top of the file.

```shell
export USER="username"
export PASSWORD="password"
```

Note: There should not be any whitespace on either side of = sign. Now, use the following command to effect the changes.

```shell
$ source .profile
```

## Handling AWS CLI credentials

For automatic deployment of lambda we use AWS CLI client. To start using it, 
you need to install dependency or aws-cli independently and configure the files located on
the path "~/.aws/". There we have 2 files:

**config**

```
[default]
region = us-east-2
output = json
```

**credentials**

```
[default]
aws_access_key_id = your_key
aws_secret_access_key = your_key
```

To do this, you can use that command:

```shell
$ aws configure
```

After that we can use:

```shell
$ make create-lambda py_name="file_name"
```

To create a lambda for the first time.

Where $file_name is the name of the .py file located in server/core/aws/lambda/.. and $file_name its name of the main
function, that should be executed in lambda. So there you should store all lambda function.

If you want use packages, you just need to add them to server/core/aws/lambda/requirements.txt.
And run:
```shell
$ make deploy-lambda-packages
```

After updating code or adding usage of new packages, you should call:
```shell
$ make update-lambda py_name="file_name"
```

## API Docs

API docs are generated by Swagger all API methods should be decorated with swagger comments. API docs page can be viewed
here:

[http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

## Deploy Lambda to AWS

1. Install [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Authenticate to AWS
```shell
$ eval $(aws ecr get-login --no-include-email | sed 's|https://||')
```
3. Create repository for docker image 
```shell
aws ecr create-repository --repository-name your-repository-name --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```
4. Make Dockerfile for lambda, see example in docker directory
5. Add command for deploy lambda, examples in the Makefile

## Use sentry.io for error tracking
Add import to your lambda 
```python
from server.core.utils import sentry_io_service  # noqa
```
Go to [sentry.io](https://sentry.io/) \
user: dev@gmail.com \
pass: 