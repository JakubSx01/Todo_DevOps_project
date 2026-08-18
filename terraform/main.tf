# Kubernetes Config Map
resource "kubernetes_config_map_v1" "app_config_map" {
  metadata {
    name      = "todo-app-config"
    namespace = "default"
  }
  data = {
    MONGODB_URI = "mongodb://mongodb:27017/"
    MONGODB_DB  = "todo_app"
  }
}

# Kubernetes Persistent Volume Claim
resource "kubernetes_persistent_volume_claim_v1" "mongodb_pvc" {
  metadata {
    name      = "mongodb-pvc"
    namespace = "default"
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
  }
}

# Kubernetes MongoDB Deployment
resource "kubernetes_deployment_v1" "mongodb_deployment" {
  wait_for_rollout = true
  metadata {
    name      = "mongodb"
    namespace = "default"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "mongodb"
      }
    }
    template {
      metadata {
        labels = {
          app = "mongodb"
        }
      }
      spec {
        automount_service_account_token = false
        enable_service_links            = false
        container {
          name  = "mongodb"
          image = "mongo:8"
          port {
            container_port = 27017
          }
          volume_mount {
            name       = "mongodb-pvc"
            mount_path = "/data/db"
          }
        }
        volume {
          name = "mongodb-pvc"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim_v1.mongodb_pvc.metadata[0].name
          }
        }
      }
    }
  }
}

# Kubernetes MongoDB Service
resource "kubernetes_service_v1" "mongodb_service" {
  wait_for_load_balancer = false
  metadata {
    name      = "mongodb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "mongodb"
    }
    port {
      port        = 27017
      target_port = 27017
    }
    type = "ClusterIP"
  }
}

resource "kubernetes_deployment_v1" "todo_app_deployment" {
  wait_for_rollout = true
  metadata {
    name      = "todo-app"
    namespace = "default"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "todo-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "todo-app"
        }
      }
      spec {
        automount_service_account_token = false
        enable_service_links            = false
        container {
          name              = "todo-app"
          image             = "ghcr.io/jakubsx01/todo_devops_project:latest"
          image_pull_policy = "Always"
          port {
            container_port = 8000
          }
          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.app_config_map.metadata[0].name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "todo_app_service" {
  wait_for_load_balancer = false
  metadata {
    name      = "todo-app"
    namespace = "default"
  }
  spec {
    selector = {
      app = "todo-app"
    }
    port {
      port        = 8000
      target_port = 8000
    }
    type = "NodePort"
  }
}