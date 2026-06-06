variable "image_tag" {
  type    = string
  default = "latest"
}

variable "repository" {
  type    = string
}


job "nightcore-dashboard-backend" {
  datacenters = ["dc1"]
  type        = "service"

  update {
    max_parallel     = 1
    min_healthy_time = "15s"
    auto_revert      = true
  }

  group "nightcore-dashboard-backend" {
    count = 2

    disconnect {
      lost_after = "40s"
    }

    task "nightcore-dashboard-backend" {
      driver = "docker"

      vault {
        role = "runner-nightcore-dashboard-backend"
      }

      identity {
        name = "vault_default"
        aud  = ["vault.io"]
        ttl  = "1h"
      }

      template {
        data = <<EOT
{{ with secret "secret/data/ci/github-registry" }}
REGISTRY_USERNAME={{ .Data.data.username }}
REGISTRY_TOKEN={{ .Data.data.token }}
{{ end }}
EOT
        destination = "secrets/registry.env"
        env         = true
        change_mode = "restart"
      }

      resources {
        cpu    = 250
        memory = 250
      }

      config {
        image = "ghcr.io/${var.repository}:${var.image_tag}"

        network_mode = "host"

        tags = [
            "traefik.enable=true",
            "traefik.http.routers.dashboard-backend.rule=Host(`${API_DOMAIN}`)",
            "traefik.http.routers.dashboard-backend.priority=10",
            "traefik.http.routers.dashboard-backend.entrypoints=websecure",
            "traefik.http.routers.dashboard-backend.service=dashboard-backend",
            "traefik.http.services.dashboard-backend.loadbalancer.server.port=${API_PORT}",
            "traefik.http.routers.dashboard-backend.tls=true",
            
            "traefik.http.middlewares.backend-ratelimit.ratelimit.average=2",
            "traefik.http.middlewares.backend-ratelimit.ratelimit.period=1s",
            "traefik.http.middlewares.backend-ratelimit.ratelimit.burst=2",
            "traefik.http.routers.dashboard-backend.middlewares=backend-ratelimit",

            "traefik.http.routers.dashboard-backend-patch.rule=Host(`${API_DOMAIN}`) && Method(`PATCH`)",
            "traefik.http.routers.dashboard-backend-patch.priority=15",
            "traefik.http.routers.dashboard-backend-patch.entrypoints=websecure",
            "traefik.http.routers.dashboard-backend-patch.service=dashboard-backend",
            "traefik.http.routers.dashboard-backend-patch.tls=true",
            "traefik.http.routers.dashboard-backend-patch.middlewares=patch-ratelimit",

            "traefik.http.middlewares.patch-ratelimit.ratelimit.average=1",
            "traefik.http.middlewares.patch-ratelimit.ratelimit.period=10s",
            "traefik.http.middlewares.patch-ratelimit.ratelimit.burst=1"
        ]

        auth {
          username       = "${REGISTRY_USERNAME}"
          password       = "${REGISTRY_TOKEN}"
        }
      }

      template {
        data = <<EOT
{{ with secret "secret/data/ci/repos/nightcore-dashboard-backend" }}
API_PORT={{ .Data.data.API_PORT }}
API_DOMAIN={{ .Data.data.API_DOMAIN }}
DASHBOARD_FRONTEND_URI={{ .Data.data.DASHBOARD_FRONTEND_URI }}
JWT_PUBLIC_KEY={{ .Data.data.JWT_PUBLIC_KEY }}
JWT_ALGORITHM={{ .Data.data.JWT_ALGORITHM }}
POSTGRES_USER={{ .Data.data.POSTGRES_USER }}
POSTGRES_PORT={{ .Data.data.POSTGRES_PORT }}
POSTGRES_PASSWORD={{ .Data.data.POSTGRES_PASSWORD }}
POSTGRES_HOST={{ .Data.data.POSTGRES_HOST }}
POSTGRES_DB={{ .Data.data.POSTGRES_DB }}
{{ end }}
EOT
        destination = "secrets/nightcore-dashboard-backend.env"
        env         = true
      }

      template {
        data = <<EOT
{{ with secret "secret/data/keydb" }}
REDIS_PASSWORD={{ .Data.data.password }}
REDIS_HOST={{ .Data.data.host }}
{{ end }}
EOT
        destination = "secrets/keydb.env"
        env         = true
      }

      logs {
        max_files     = 3
        max_file_size = 10
      }

    }
  }
}