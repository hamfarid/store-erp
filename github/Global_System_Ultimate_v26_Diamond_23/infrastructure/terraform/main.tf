# Infrastructure as Code (Terraform)
# Provider: AWS
provider "aws" {
  region = "us-east-1"
}

# VPC Resource
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "GlobalSystemVPC"
  }
}
