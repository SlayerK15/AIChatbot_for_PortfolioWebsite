output "ecs_public_ip" {
  value = aws_ecs_task_definition.chatbot_task.network_configuration[0].assign_public_ip
}
output "ecs_public_url" {
  value = "http://${aws_ecs_task_definition.chatbot_task.network_configuration[0].assign_public_ip}:80"
}
