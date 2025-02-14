output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.chatbot_cluster.name
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.chatbot_service.name
}

output "ecs_task_definition_arn" {
  description = "The ARN of the ECS task definition"
  value       = aws_ecs_task_definition.chatbot_task.arn
}

output "ecs_public_ip" {
  description = "The public IP assigned to the ECS service"
  value       = aws_lb.chatbot_lb.dns_name
}

output "ecs_public_url" {
  description = "The public URL for accessing the chatbot service"
  value       = "http://${aws_lb.chatbot_lb.dns_name}:80"
}
