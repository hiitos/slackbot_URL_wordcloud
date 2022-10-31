# tfvars
variable project_id {}

# jsonファイルのパスをcredentialsに設定する
provider "google" {
  credentials = "${file("<your-credential-file-path>")}"
  project = var.project_id
  region  = var.project_region
  zone    = var.project_zone
}

# Cloud Functionsにアップロードするファイルをzipに固める。
data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "./src"
  output_path = "./src.zip"
}
 
# zipファイルをアップロードするためのbucketを作成
resource "google_storage_bucket" "bucket" {
  name          = bucket_name
  location      = var.project_region
  storage_class = "STANDARD"
}
 
# zipファイルをアップロードする
resource "google_storage_bucket_object" "packages" {
  name   = "packages/functions.${data.archive_file.function_archive.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.function_archive.output_path
}
 
#Cloud Functions本体
resource "google_cloudfunctions_function" "function" {
  name                  = "sample-function"
  runtime               = "nodejs16"
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.packages.name
  trigger_http          = true
  available_memory_mb   = 512
  timeout               = 120
  entry_point           = run
}
