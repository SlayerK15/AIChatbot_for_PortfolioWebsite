output "ecs_cluster_id" {
  description = "ECS Cluster ID"
  value       = aws_ecs_cluster.chatbot_cluster.id
}

output "ecs_service_id" {
  description = "ECS Service ID"
  value       = aws_ecs_service.chatbot_service.id
}

output "ecs_task_definition_arn" {
  description = "ECS Task Definition ARN"
  value       = aws_ecs_task_definition.chatbot_task.arn
}

output "security_group_id" {
  description = "Security Group ID"
  value       = aws_security_group.ecs_sg.id
}

output "iam_role_arn" {
  description = "IAM Role ARN for ECS Tasks"
  value       = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_public_url" {
  description = "Public URL of the chatbot service"
  value       = "http://${aws_ecs_service.chatbot_service.id}:80"
}
