# ☁️ Deploy no Google Cloud Functions — Guia Completo

Este documento explica como fazer o deploy manual do seu ETL Serverless no Google Cloud.

---

## 🚀 1. Autenticar no Google Cloud

```bash
gcloud auth login
Selecionar o projeto:
```
```bash
Copiar código
gcloud config set project <SEU_PROJETO>
```
---

## 📁 2. Estrutura necessária

O deploy envia APENAS os arquivos necessários:

```bash
Copiar código
src/
requirements.txt
deploy/deploy.sh
```

---

## ⚙️ 3. Variáveis obrigatórias no Cloud Functions
Você precisará definir:

GCP_PROJECT_ID

BIGQUERY_DATASET

BIGQUERY_TABLE

---

## 📦 4. Deploy manual

```bash
Copiar código
gcloud functions deploy gcp_etl_pipeline \
  --runtime python311 \
  --trigger-http \
  --entry-point main \
  --region southamerica-east1 \
  --set-env-vars GCP_PROJECT_ID=<projeto>,BIGQUERY_DATASET=<dataset>,BIGQUERY_TABLE=<tabela> \
  --allow-unauthenticated
```

---

## 🌍 5. Obter URL da função

```bash
Copiar código
gcloud functions describe gcp_etl_pipeline \
  --region southamerica-east1 \
  --format="value(httpsTrigger.url)"
```

---

## 🔍 6. Logs da função

```bash
Copiar código
gcloud functions logs read gcp_etl_pipeline --region=southamerica-east1
```

---

## 🔄 7. Redeploy rápido

```bash
Copiar código
bash deploy/deploy.sh
```

### 📌 Observação Importante

A função utiliza:

- BigQuery
- Cloud Functions
- Secret Manager (Opcional)
- API Externa (IBGE)

Certifique-se de que o BigQuery e a conta de serviço tenham permissão:

- java
- Copiar código
- BigQuery Data Editor
- BigQuery Job User
- Secret Manager Accessor (se usar secrets)

---

## 🧩 Dúvidas?

Fale comigo para gerar um deploy CI/CD no GitHub Actions.