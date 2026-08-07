#!/bin/bash

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update

helm upgrade --install monitoring \
  prometheus-community/kube-prometheus-stack \
  -f values.yaml \
  -n monitoring \
  --create-namespace \
  --wait \
  --timeout 10m
