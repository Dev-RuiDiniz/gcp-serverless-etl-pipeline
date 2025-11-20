#!/bin/bash

set -e

echo "---------------------------------------"
echo " 🚀 Deploy automático — Cloud Functions"
echo "---------------------------------------"

# === CONFIGURAÇÕES ===
FUNCTION_NAME="gcp_etl_pipeline"
ENTRY_POINT="main"
REGION="southamerica-east1"
RUNTIME="python311"

# Carregar variáveis do .env
if [ -f ".env" ]; then
  echo "Carregando variáveis do .env..."
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️  .env não encontrado. Continuando sem variáveis locais."
fi

# === VALIDAÇÃO DE VARIÁVEIS ===
REQUIRED_VARS=("GCP_PROJECT_ID" "BIGQUERY_DATASET" "BIGQUERY_TABLE")

for var in "${REQUIRED_VARS[@]}"; do
  if [[ -z "${!var}" ]]; then
    echo "❌ ERRO: Variável de ambiente ausente: $var"
    exit 1
  fi
done

echo "✔ Variáveis de ambiente validadas."

# === INICIAR DEPLOY ===
echo "📦 Enviando função para Cloud Functions..."

gcloud functions deploy "$FUNCTION_NAME" \
  --runtime "$RUNTIME" \
  --trigger-http \
  --entry-point "$ENTRY_POINT" \
  --region "$REGION" \
  --project "$GCP_PROJECT_ID" \
  --set-env-vars GCP_PROJECT_ID="$GCP_PROJECT_ID",BIGQUERY_DATASET="$BIGQUERY_DATASET",BIGQUERY_TABLE="$BIGQUERY_TABLE" \
  --allow-unauthenticated

echo "---------------------------------------"
echo "🎉 Deploy concluído com sucesso!"
echo "🌍 URL pública:"
gcloud functions describe "$FUNCTION_NAME" --region "$REGION" --format="value(httpsTrigger.url)"
echo "---------------------------------------"
