variable "project" {
  description = "Project"
  default     = "de-zoomcamp-2-485306"
}

variable "region" {
  description = "Region"
  default     = "asia-south1" 
}

variable "location" {
  description = "Project Location"
  default     = "asia-south1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "market_radar_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "market_radar_datalake_lakshya" # Must be globally unique
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
