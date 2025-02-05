#!/bin/bash

# Define the number of instances and starting port
INSTANCES=2
START_PORT=5000

for ((i=1; i<=INSTANCES; i++))
do
  INSTANCE="instance-$i"
  PORT=$((START_PORT + i - 1))
  EXTERNAL_PORT=$((PORT + 10000))  # External port for LoadBalancer

  # Generate Deployment YAML
  sed -e "s/{{INSTANCE}}/$INSTANCE/g" -e "s/{{PORT}}/$PORT/g" deployment-template.yaml > deployment-$INSTANCE.yaml

  # Generate Service YAML
  sed -e "s/{{INSTANCE}}/$INSTANCE/g" -e "s/{{PORT}}/$PORT/g" -e "s/{{EXTERNAL_PORT}}/$EXTERNAL_PORT/g" service-template.yaml > service-$INSTANCE.yaml

  # Apply the manifests
  kubectl apply -f deployment-$INSTANCE.yaml
  kubectl apply -f service-$INSTANCE.yaml
done