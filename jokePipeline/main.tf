# ======== pipeline ======== #

provider "aws" {
  region = var.region
}

module "eventbridge" {
  source     = "terraform-aws-modules/eventbridge/aws"
  version    = "1.17.2"
  create_bus = false
  role_name  = "${var.function_name}-eventbridge"

  rules = {
    crons = {
      description         = "Trigger for a Lambda"
      schedule_expression = "rate(5 minutes)"
    }
  }

  targets = {
    crons = [
      {
        name  = "${var.function_name}-cron"
        arn   = module.lambda.lambda_function_arn
        input = jsonencode({ "job" : "cron-by-rate" })
      }
    ]
  }
}


module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 2.0"

  function_name = "${var.function_name}_lambda"
  handler       = "${var.function_name}.lambda_handler"
  runtime       = "python3.8"

  create_package         = false
  local_existing_package = "${var.function_name}.zip"
  layers                 = ["${var.lambda_arn}:1"]

  create_current_version_allowed_triggers = false
  allowed_triggers = {
    ScanAmiRule = {
      principal  = "events.amazonaws.com"
      source_arn = module.eventbridge.eventbridge_rule_arns["crons"]
    }
  }

  attach_policy_json = true
  policy_json        = <<-EOT
    {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect" : "Allow",
            "Action" : [
              "s3:PutObject",
              "s3:GetObject",
              "s3:ListBucket",
              "s3:DeleteObject"
            ],
            "Resource" : [
              "arn:aws:s3:::${var.bucket_name}*"
            ]
          }
        ]
    }
  EOT
}

