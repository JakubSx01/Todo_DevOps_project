variable "namespace" {
  description = "Kubernetes namespace for appliaction resources"
  type        = string
  default     = "todo"
}

variable "app_image" {
  description = "Docker image used by the Todo application"
  type        = string
  default     = "ghcr.io/jakubsx01/todo_devops_project:latest"
}

variable "base_path" {
  description = "Base path for the Todo application"
  type        = string
  default     = "/todo-devops-project"
}

variable "mongodb_image" {
  description = "Docker image used by the MongoDB database"
  type        = string
  default     = "mongo:8"
}

variable "app_replicas" {
  description = "Number of replicas for the Todo application"
  type        = number
  default     = 1
}

variable "mongodb_replicas" {
  description = "Number of replicas for the MongoDB database"
  type        = number
  default     = 1
}

variable "mongodb_storage_size" {
  description = "Storage size for the MongoDB database"
  type        = string
  default     = "1Gi"
}

