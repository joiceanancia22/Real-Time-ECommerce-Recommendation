# Real-Time E-Commerce Recommendation & Sales Analytics System

A Big Data Management mini project that performs real-time
e-commerce data processing using Apache Spark Structured Streaming,
Neo4j, Docker, and Python. The system processes streaming
purchase events, performs ETL, analyzes customer behavior, detects
trending products, and generates personalized product recommendations.

## Features

-   Real-time data streaming
-   Apache Spark Structured Streaming
-   ETL using PySpark
-   Neo4j graph database integration
-   Product recommendation engine
-   Trending product analytics
-   Co-purchase analysis
-   Dashboard visualization
-   Dockerized deployment

## Technologies Used

-   Python
-   Apache Spark
-   PySpark
-   Neo4j
-   Docker & Docker Compose
-   Matplotlib

## Project Structure

``` text
ecommerce/
│── spark_jobs/
│   └── stream_processor.py
│
│── streaming/
│   └── data_generator.py
│
│── data/
│   └── stream/
│
│── dashboard.py
│── visualize_results.py
│── docker-compose.yml
│── Dockerfile
│── Dockerfile.generator
│── Dockerfile.ui
│── requirements.txt
│── trending.png
│── copurchase.png
│── user_recommendation.png
```

## How to Run

``` bash
docker-compose up --build
```

Start the streaming data generator, execute the Spark streaming job, and
open the dashboard to view analytics and recommendations.

## Workflow

Streaming Data → Spark Structured Streaming → ETL → Neo4j Graph
Database → Analytics → Dashboard & Visualizations**

## Team Members

-   Dileep Ram
-   Joice Anancia
-   Madhu Vishahan

Academic Year: 2025--2026
