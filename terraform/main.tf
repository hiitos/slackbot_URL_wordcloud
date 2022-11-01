# tfvars
variable "gcp_project_data" {}
variable "billing_id" {}
variable project_region {}
variable project_zone {}

#### プロジェクトの作成 ####
resource "google_project" "gcp_project" {
  name                = var.gcp_project_data
  project_id          = var.gcp_project_data
  billing_account     = var.billing_id
  auto_create_network = false
}

# jsonファイルのパスをcredentialsに設定する
provider "google" {
  project = var.gcp_project_data
  region  = var.project_region
  zone    = var.project_zone
}

# Cloud Functionsにアップロードするファイルをzipに固める。
data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "./src"
  output_path = "./src.zip"
}
 
# # zipファイルをアップロードするためのbucketを作成
# resource "google_storage_bucket" "bucket" {
#   name          = bucket_name
#   location      = var.project_region
#   storage_class = "STANDARD"
# }
 
# # zipファイルをアップロードする
# resource "google_storage_bucket_object" "packages" {
#   name   = "packages/functions.${data.archive_file.function_archive.output_md5}.zip"
#   bucket = google_storage_bucket.bucket.name
#   source = data.archive_file.function_archive.output_path
# }
 
# #Cloud Functions本体
# resource "google_cloudfunctions_function" "function" {
#   name                  = "sample-function"
#   runtime               = "nodejs16"
#   source_archive_bucket = google_storage_bucket.bucket.name
#   source_archive_object = google_storage_bucket_object.packages.name
#   trigger_http          = true
#   available_memory_mb   = 512
#   timeout               = 120
#   entry_point           = run
# }
