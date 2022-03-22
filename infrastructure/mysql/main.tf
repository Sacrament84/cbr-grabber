provider "google" {
  project      = var.project_id
  region       = var.region
}

resource "google_sql_database_instance" "dev" {
  name = "dev-instance"
  database_version = "MYSQL_5_7"
  region       = var.region
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
  }
}
resource "google_sql_database_instance" "prod" {
  name = "prod-instance"
  database_version = "MYSQL_5_7"
  region       = var.region
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
  }
}
resource "google_sql_database" "staging" {
  name      = "staging"
  instance  = google_sql_database_instance.dev.name
  charset   = "utf8"
  collation = "utf8_general_ci"
}
resource "google_sql_database" "prod" {
  name      = "production"
  instance  = google_sql_database_instance.prod.name
  charset   = "utf8"
  collation = "utf8_general_ci"
}
resource "google_sql_user" "users" {
  name     = "staging"
  instance = google_sql_database_instance.dev.name
  host     = "%"
  password = "var.mysql_staging_password"
}
resource "google_sql_user" "production" {
  name     = "production"
  instance = google_sql_database_instance.prod.name
  host     = "%"
  password = "var.mysql_production_password"
}
