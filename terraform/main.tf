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

# Clave SSH para conectar por deploy automático
resource "aws_key_pair" "deploy_key" {
  key_name   = "devops-deploy-key"
  public_key = var.ssh_public_key
}

# Security Group - reglas de firewall
resource "aws_security_group" "devops_sg" {
  name        = "devops-project-sg"
  description = "Security group para el proyecto DevOps"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App Flask"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "devops-project-sg"
  }
}

# Instancia EC2 gratuita (free tier)
resource "aws_instance" "devops_server" {
  ami                    = "ami-0c7217cdde317cfec"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deploy_key.key_name
  vpc_security_group_ids = [aws_security_group.devops_sg.id]

  tags = {
    Name = "devops-project-server"
  }
}

output "server_ip" {
  value = aws_instance.devops_server.public_ip
}
