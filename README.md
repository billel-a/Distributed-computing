# Distributed-computing
# Project Master1 Distributed computing

# Building docker images: 

docker build -t flasksql .

docker tag ImageID billela/flasksql:1

docker push billela/flasksql:1

docker build -t flasksql .

docker tag ImageID billela/flasknews:1

docker push billela/flasknews:1

# kubernetes : 
minikube start

kubectl apply -f mysql-secret.yaml

kubectl apply -f mysql-storage.yaml

kubectl apply -f mysql-deployment.yaml

kubectl apply -f mysql-serviceNodePort.yaml


kubectl get secrets

kubectl get PersistentVolumes

kubectl get PersistentVolumeClaims

kubectl get deployments

kubectl get services

kubectl get pods


kubectl exec --stdin --tty mysql-74799d694c-vhsrw -- mysql -proot


create database db;

use db;

CREATE TABLE accounts(
    username varchar(20) NOT NULL ,
    email varchar(20) NOT NULL ,
    password varchar(20) NOT NULL ,
    PRIMARY KEY (username)
);

INSERT INTO accounts VALUES ( "a", "a@gmail.com", 'a');

exit


kubectl apply -f flask-mysql-deployment.yaml

kubectl apply -f flask-mysql-service.yaml


kubectl apply -f news-deployment.yaml

kubectl apply -f news-service.yaml


minikube service news-service --url


kubectl apply -f news-lb

minikube service news-lb --url


kubectl apply -f app-ingress.yaml


Minikube addons enable ingress-dns


kubectl delete --all ingress

kubectl delete --all pods

kubectl delete --all services

kubectl delete --all deployments

kubectl delete --all PersistentVolumeClaims

kubectl delete --all PersistentVolumes

kubectl delete --all secrets

