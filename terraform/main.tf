resource "random_string" "suffix" {
  length  = 8
  special = false
}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  cluster_name = "intranet-${random_string.suffix.result}"
}
