# # Create Milvus file
# $ mkdir -p /home/$USER/milvus/conf
# $ cd /home/$USER/milvus/conf
# $ wget https://raw.githubusercontent.com/milvus-io/milvus/v0.8.0/core/conf/demo/server_config.yaml
# $ wget https://raw.githubusercontent.com/milvus-io/milvus/v0.8.0/core/conf/demo/log_config.conf
sudo systemctl start milvus
sudo systemctl start milvus-etcd
sudo systemctl start milvus-minio
