# Planted IaC fixture: open ingress, public unencrypted bucket.
terraform {
  required_version = ">= 1.5"
}

resource "aws_security_group" "gateway" {
  name        = "orderlab-gateway"
  description = "Gateway ingress"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "orders" {
  bucket = "orderlab-orders"
  acl    = "public-read"
}
