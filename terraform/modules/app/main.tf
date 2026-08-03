
resource "aws_security_group" "movie-security" {
    name = "movie-security"
        ingress{
            from_port = 22
            to_port = 22
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        ingress{
            from_port = 80
            to_port = 80
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        ingress{
            from_port = 6443
            to_port = 6443
            protocol = "tcp"
            cidr_blocks = ["2.132.201.73/32"]
        }

        ingress{
            from_port = 443
            to_port = 443
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        egress{
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }

data "aws_ami" "ubuntu" {
    most_recent = true
    owners = ["099720109477"]
    filter{
        name = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
    }
}

resource "aws_instance" "movie" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.medium"

  key_name = var.key_name

  vpc_security_group_ids = [aws_security_group.movie-security.id]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name = "movie-server"
  }
}


resource "aws_eip" "movie"{
    instance = aws_instance.movie.id
}