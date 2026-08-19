output "app_service_name" {
  value = kubernetes_service_v1.todo_app_service.metadata[0].name
}

output "app_node_port" {
  value = kubernetes_service_v1.todo_app_service.spec[0].port[0].node_port
}

output "namespace" {
  value = var.namespace
}
