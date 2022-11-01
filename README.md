# Slack bot word cloud

```
docker compose build
```

```
docker compose up
```


## pythonコンテナ
```
docker exec -it python3 /bin/sh
```

## gcloud 認証
```
docker exec -it tf_container /bin/sh
```

```
docker compose run --rm gcp_container gcloud auth application-default login --project <使用するプロジェクトID>
```

## terraformコンテナ
gcloud認証をした後ではないとできない
```
docker exec -it tf_container /bin/sh
```
```
terraform init
```
```
terraform plan
```
```
terraform apply
```

