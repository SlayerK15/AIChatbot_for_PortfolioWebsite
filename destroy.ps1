# Set AWS Region
$AWS_REGION = "ap-south-1"
Write-Host "🚀 Starting Infrastructure Deletion in Region: $AWS_REGION"

# 1️⃣ Delete ECS Service
Write-Host "🛑 Deleting ECS Service..."
aws ecs update-service --cluster portfolio-chatbot-cluster --service portfolio-chatbot-service --desired-count 0 --region $AWS_REGION
aws ecs delete-service --cluster portfolio-chatbot-cluster --service portfolio-chatbot-service --force --region $AWS_REGION

# 2️⃣ Delete ECS Cluster
Write-Host "🛑 Deleting ECS Cluster..."
aws ecs delete-cluster --cluster portfolio-chatbot-cluster --region $AWS_REGION

# 3️⃣ Get & Delete Security Groups
Write-Host "🛑 Deleting Security Groups..."
$SECURITY_GROUPS = aws ec2 describe-security-groups --region $AWS_REGION --query "SecurityGroups[*].GroupId" --output text
foreach ($SG in $SECURITY_GROUPS -split "`n") {
    Write-Host "Deleting Security Group: $SG"
    aws ec2 delete-security-group --group-id $SG --region $AWS_REGION
}

# 4️⃣ Get & Delete Load Balancers
Write-Host "🛑 Deleting Load Balancers..."
$LOAD_BALANCERS = aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[*].LoadBalancerArn" --output text
foreach ($LB in $LOAD_BALANCERS -split "`n") {
    Write-Host "Deleting Load Balancer: $LB"
    aws elbv2 delete-load-balancer --load-balancer-arn $LB --region $AWS_REGION
}

# 5️⃣ Get & Delete IAM Role (Task Execution Role)
Write-Host "🛑 Deleting IAM Role..."
aws iam detach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam delete-role --role-name ecsTaskExecutionRole

# 6️⃣ Deregister ECS Task Definition
Write-Host "🛑 Deregistering ECS Task Definition..."
$TASK_DEFINITIONS = aws ecs list-task-definitions --region $AWS_REGION --query "taskDefinitionArns[*]" --output text
foreach ($TASK in $TASK_DEFINITIONS -split "`n") {
    Write-Host "Deregistering Task Definition: $TASK"
    aws ecs deregister-task-definition --task-definition $TASK --region $AWS_REGION
}

Write-Host "✅ Infrastructure Deletion Complete!"
