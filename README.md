# 🚀 Pipeline ETL Serverless — Google Cloud (BigQuery + Cloud Functions)

Este projeto implementa uma **Pipeline ETL totalmente automatizada e serverless** utilizando o ecossistema do **Google Cloud Platform (GCP)**.

O pipeline foi desenvolvido com foco em boas práticas, arquitetura modular e **Programação Orientada a Objetos (POO)** aplicadas ao contexto de Engenharia de Dados.

---

## 📌 Objetivos do Pipeline
- Consumir dados de uma **API pública** (IBGE, moedas, clima, etc.).
- Realizar **limpeza e transformação** utilizando *Pandas*.
- Carregar dados automaticamente no **BigQuery**.
- Integrar o resultado com **Looker Studio (Data Studio)** para dashboards automatizados.
- Operar 100% em **Cloud Functions**, sem servidores.

---

## 🏗️ Arquitetura Geral

API Externa → Cloud Function (Extract)
↓
Cloud Function (Transform)
↓
BigQuery (Load)
↓
Looker Studio — Dashboard Automático

yaml
Copiar código

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|----------|-------------|
| Linguagem | Python 3.11 |
| Cloud | Cloud Functions, BigQuery, Secret Manager |
| Bibliotecas | pandas, requests, google-cloud-bigquery |
| DevOps | GitHub, .gitignore, virtualenv |
| Padrões | POO, SOLID, Camadas ETL isoladas |

---

## 📂 Estrutura de Pastas (versão inicial)

```txt
.
├── src/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── exceptions.py
│   ├── etl/
│   │   ├── extractor.py
│   │   ├── transformer.py
│   │   └── loader.py
│   ├── services/
│   │   ├── bigquery_service.py
│   │   ├── api_service.py
│   │   └── secrets_service.py
│   ├── main.py
│   ├── cloud_function_handler.py
│   └── utils/
│       └── validators.py
│
├── tests/
│   ├── test_extractor.py
│   ├── test_transformer.py
│   └── test_loader.py
│
├── README.md
├── requirements.txt
├── .gitignore
├── estrutura.txt
└── deploy/
    ├── deploy.sh
    └── gcloud_instructions.md
```
---

## 🚀 Execução Local

```bash

python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install -r requirements.txt

python src/main.py
```
---

## ☁️ Deploy na Cloud Function

Deploy manual:

```bash

gcloud functions deploy etl_pipeline \
  --runtime python311 \
  --trigger-http \
  --entry-point main \
  --region southamerica-east1
```
---

## 📊 Dashboard Automático (Looker Studio)

Após o carregamento no BigQuery, você pode conectar a tabela diretamente ao Looker e gerar:

- Relatórios automáticos
- Filtros dinâmicos
- Atualização programada

---

## 👨‍💻 Autor
**Rui Francisco de Paula Inácio Diniz**
Engenheiro de Software | Desenvolvedor Back-end Python | Analista de Dados
GitHub: https://github.com/Dev-RuiDiniz
LinkedIn: https://linkedin.com/in/rui-francisco
