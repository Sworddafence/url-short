#!/bin/bash

# Check if a number is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <number_of_instances>"
  exit 1
fi

# Get the number of instances from the argument
num_instances=$1

# Loop to create the specified number of Docker containers
for ((i=0; i<num_instances; i++))
do
  port=$((5001 + i))
  echo "Starting Docker container on port $port"
  docker run -d -p $port:5001 -e FLASK_PORT=$port url-shortener:latest 
done

echo "$num_instances Docker containers have been started."
