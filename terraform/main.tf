provider "aws" {
  region = "ap-south-1"
}

# Use existing VPC and subnets
variable "vpc_id" {
  default = "vpc-08cd1083d45e7d9df"
}

variable "subnet_ids" {
  default = [
    "subnet-0650cd04fd6535c87",
    "subnet-0bab34170eb4d6a5f",
    "subnet-010ce0c3753e7cffb"
  ]
}

resource "aws_security_group" "ecs_sg" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
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
}

# Create ECS Cluster
resource "aws_ecs_cluster" "chatbot_cluster" {
  name = "portfolio-chatbot-cluster"
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "chatbot_task" {
  family                   = "portfolio-chatbot-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "portfolio-chatbot"
      image     = "slayerop15/portfolio-chatbot:latest"
      cpu       = 512
      memory    = 1024
      essential = true
      environment = [
      {
        name  = "API_KEY"
        value = "${var.API_KEY}"
      }
      ],
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

# Create ECS Service
resource "aws_ecs_service" "chatbot_service" {
  name            = "portfolio-chatbot-service"
  cluster         = aws_ecs_cluster.chatbot_cluster.id
  task_definition = aws_ecs_task_definition.chatbot_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}

# IAM Role for ECS Task Execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Attach policies to the ECS Task Execution Role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
