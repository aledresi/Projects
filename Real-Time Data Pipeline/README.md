# Real-Time Mobile App Logging Pipeline

This project simulates a real-time mobile application logging system using **Apache NiFi**, **Apache Kafka**, and **Apache Hadoop**. 

The pipeline handles continuously generated, messy streaming data coming from a Python script. To simulate a real-world streaming environment, the generated logs intentionally contain missing values, duplicate records, invalid timestamps, corrupted values, and inconsistent numeric fields.

Inside NiFi, the data is ingested continuously, split into smaller chunks, transformed from CSV to JSON, cleaned, validated, deduplicated, published into Kafka topics, consumed again from Kafka, and finally stored into HDFS in a partitioned structure.

The main goal of the pipeline is to demonstrate stable streaming ingestion, real-time processing, data quality handling, Kafka integration, and scalable Hadoop storage.

---

## 🏗️ System Architecture

![System Architecture](./5.%20Architecture%20Diagram/architecture%20diagram.png)

---

## 🔄 Data Flow & Processor Explanation

### 1. Ingestion & Chunking
* **ListFile & FetchFile:** Used to continuously monitor the incoming directory and ingest newly generated streaming files automatically.
* **SplitText:** Used to divide incoming files into smaller chunks close to the required 64 KB limit. This improves memory handling and allows smoother streaming behavior inside NiFi.

### 2. Transformation & Content Handling
* **ConvertRecord:** Converts the CSV records into JSON format using `CSVReader` and `JsonRecordSetWriter`.
* **UpdateAttribute (Content Type Handling):** Some FlowFiles appeared in a hexadecimal view because the `mime.type` attribute was missing. To fix this, an `UpdateAttribute` processor was implemented to explicitly set the mime type, converting them into standard JSON files for clear visualization.

### 3. Data Quality & Cleansing
* **QueryRecord (Cleaning Stage):** Used to clean invalid and incomplete data. This stage filters out null values, invalid numeric fields, and malformed timestamps.
* **QueryRecord (Timestamp Standardization):** Normalizes different timestamp formats into a unified format (`yyyy-MM-dd HH:mm:ss`). Invalid timestamps are dynamically replaced with the current processing timestamp.
* **DeduplicateRecord:** Removes duplicated records before publishing them into Kafka. The duplicate check is based strictly on the `log_id` field.

### 4. Messaging & Storage Ingestion
* **PublishKafka:** After undergoing cleaning and validation, the final JSON records are published into the Kafka topic `mobile_app_logs`.
* **ConsumeKafka:** A separate, decoupled NiFi consumer continuously consumes the Kafka messages for downstream storage.
* **PutHDFS:** The final cleaned JSON records are stored inside HDFS using date-based partitioning.

---

## 📊 Apache NiFi Workflow Canvas

# Apache NiFi Workflow Canvas in groubs
![Apache NiFi Flow](./2.%20NiFi%20Flow/big%20picture%20flow.png)
# Entire NiFi Workflow Canvas
![Apache NiFi Flow](./2.%20NiFi%20Flow/ALL%20NIFI%20FLOW%20.png)
