# Enables the SQL Admin API for the project.
resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"

  # Prevents the API from being disabled when the resource is destroyed.
  disable_on_destroy = false
}

resource "google_sql_database_instance" "datawarehouse" {
  name                = "datawarehouse"
  database_version    = "MYSQL_8_4"
  region              = local.region
  deletion_protection = false

  settings {
    edition = "ENTERPRISE"
    tier = "db-custom-1-3840"
    disk_autoresize = false
    disk_size = 100

    database_flags {
      name  = "cloudsql_iam_authentication"
      value = "on"
    }

    ip_configuration {
      ipv4_enabled    = true
      ssl_mode        = "ENCRYPTED_ONLY"
    }

    insights_config {
      query_insights_enabled = true
    }
  }

  depends_on = [ google_project_service.sqladmin ]
}
