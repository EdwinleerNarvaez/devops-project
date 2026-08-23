# Proveedor AWS
# Le dice a Terraform que vamos a trabajar con AWS en la región us-east-1
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Instancia EC2 gratuita (free tier)
# Es el servidor donde va a correr nuestra app
resource "aws_instance" "devops_server" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 en us-east-1
  instance_type = "t2.micro"               # Free tier

  tags = {
    Name = "devops-project-server"
  }
}

# Output: muestra la IP pública del servidor al terminar
output "server_ip" {
  value = aws_instance.devops_server.public_ip
}
