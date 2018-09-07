#!/bin/bash
docker pull gunanksood/producer_image
docker pull gunanksood/consumer_image
docker run -p 5000:5000 -d gunanksood/producer_image
docker run -p 5001:5001 -d gunanksood/consumer_image
docker-compose up -d
