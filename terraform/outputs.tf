output "ecs_public_ip" {
  description = "Public IP of the ECS Task"
  value       = aws_ecs_task.portfolio_chatbot.network_configuration[0].assign_public_ip
}

output "ecs_public_url" {
  description = "Public URL of the ECS Task"
  value       = "http://${aws_ecs_task.portfolio_chatbot.network_configuration[0].assign_public_ip}:80"
}
