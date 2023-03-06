# Serverless_Pipeline
Simplest solution to write APIs results to S3

This project allows you to quickly get data from an API and write the output to S3, with a minimal architecture.
Via a terraform script each pipeline is composed of:
- a lambda function that will call the api and write the result
- an eventbridge cron that will trigger the lambda
- a specific S3 logic to write the files

## The example of a joke pipeline

Let's deploy a first pipeline:

```
pipenv shell
cd jokePipeline
```

you can first open the explore.ipynb notebook to test your API calls. 
When you are satisfied with the result, update lambda.py with your function call and parameters: url, bucket_name, api_name.

Once done, let's deploy 🚀

```
# create lambda layer with python modules
cd ../
sh lambda_layer.sh
# note the *layer arn* value printed back

cd jokePipeline
zip jokes.zip jokes.py

# update variables.tf with your configuration
terraform init
terraform apply
```

## Adding custom pipeline

Duplicate the template pipeline to your custom name and follow the same instructions.
