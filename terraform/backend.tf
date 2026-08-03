terraform {
  backend "s3" {
    bucket = "my-movie-tfstate-bucket"
    key    = "project/terraform.tfstate"
    region = "eu-north-1"
  }
}