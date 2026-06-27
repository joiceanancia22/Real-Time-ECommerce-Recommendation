from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from neo4j import GraphDatabase
import pandas as pd

# ---------------------------
# SPARK SESSION
# ---------------------------
spark = SparkSession.builder \
    .appName("EcommerceStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ---------------------------
# SCHEMA
# ---------------------------
schema = "user_id INT, product_id INT, action STRING, timestamp DOUBLE"

# ---------------------------
# READ STREAM
# ---------------------------
df = spark.readStream \
    .schema(schema) \
    .json("file:///app/data/stream")

# ---------------------------
# FILTER PURCHASES
# ---------------------------
purchases = df.filter(col("action") == "purchase")
print(purchases)
# ---------------------------
# TRENDING PRODUCTS (FAST)
# ---------------------------
trending = purchases.groupBy("product_id").count()
print(trending)
trending.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 10) \
    .trigger(processingTime="3 seconds") \
    .start()

# ---------------------------
# NEO4J CONNECTION
# ---------------------------
driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "madhu0607")
)

# ---------------------------
# CORE LOGIC
# ---------------------------
def write_to_neo4j(batch_df, batch_id):
    print(f"\nProcessing batch {batch_id}")

    pdf = batch_df.toPandas()

    if pdf.empty:
        print("Empty batch")
        return

    # ---------------------------
    # USER → PRODUCT RELATION
    # ---------------------------
    with driver.session() as session:
        for _, row in pdf.iterrows():
            session.run("""
                MERGE (u:User {id: $user})
                MERGE (p:Product {id: $product})
                MERGE (u)-[:BOUGHT]->(p)
            """, user=int(row["user_id"]), product=int(row["product_id"]))

    # ---------------------------
    # CO-PURCHASE LOGIC
    # ---------------------------
    merged = pdf.merge(pdf, on="user_id")
    merged = merged[merged["product_id_x"] != merged["product_id_y"]]

    grouped = merged.groupby(
        ["product_id_x", "product_id_y"]
    ).size().reset_index(name="count")

    print("Top co-purchases:")
    print(grouped.head())

    # ---------------------------
    # WRITE PRODUCT RELATIONS
    # ---------------------------
    with driver.session() as session:
        for _, row in grouped.iterrows():
            session.run("""
                MERGE (p1:Product {id: $p1})
                MERGE (p2:Product {id: $p2})
                MERGE (p1)-[:BOUGHT_WITH {score: $count}]->(p2)
            """,
            p1=int(row["product_id_x"]),
            p2=int(row["product_id_y"]),
            count=int(row["count"]))

# ---------------------------
# STREAM EXECUTION
# ---------------------------
purchases.writeStream \
    .trigger(processingTime="3 seconds") \
    .foreachBatch(write_to_neo4j) \
    .start() \
    .awaitTermination()
