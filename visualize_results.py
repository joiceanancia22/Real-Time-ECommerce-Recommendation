from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# CONNECT TO NEO4J
# ---------------------------
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "madhu0607")
)

# ---------------------------
# 1️⃣ TRENDING PRODUCTS
# ---------------------------
def get_trending():
    query = """
    MATCH (u:User)-[:BOUGHT]->(p:Product)
    RETURN p.id AS product, COUNT(*) AS purchases
    ORDER BY purchases DESC
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query)
        data = [(r["product"], r["purchases"]) for r in result]

    return pd.DataFrame(data, columns=["product", "count"])


# ---------------------------
# 2️⃣ CO-PURCHASE RELATIONSHIPS
# ---------------------------
def get_copurchase():
    query = """
    MATCH (p1:Product)-[r:BOUGHT_WITH]->(p2:Product)
    RETURN p1.id AS product_A, p2.id AS product_B, r.score AS strength
    ORDER BY strength DESC
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query)
        data = [(r["product_A"], r["product_B"], r["strength"]) for r in result]

    return pd.DataFrame(data, columns=["A", "B", "strength"])


# ---------------------------
# 3️⃣ USER RECOMMENDATION
# ---------------------------
def get_user_recommendations(user_id):
    query = """
    MATCH (u:User {id: $uid})-[:BOUGHT]->(p1)-[:BOUGHT_WITH]->(p2)
    RETURN DISTINCT p2.id AS product
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query, uid=user_id)
        data = [r["product"] for r in result]

    return pd.DataFrame(data, columns=["product"])


# ---------------------------
# 📊 PLOT FUNCTIONS
# ---------------------------
def plot_trending(df):
    plt.figure()
    plt.bar(df["product"].astype(str), df["count"])
    plt.title("🔥 Trending Products")
    plt.xlabel("Product ID")
    plt.ylabel("Purchases")

    plt.savefig("trending.png")
    print("✅ Saved: trending.png")

def plot_copurchase(df):
    labels = df["A"].astype(str) + "-" + df["B"].astype(str)

    plt.figure()
    plt.bar(labels, df["strength"])
    plt.title("🧠 Co-Purchase Strength")
    plt.xlabel("Product Pairs")
    plt.ylabel("Score")
    plt.xticks(rotation=45)

    plt.savefig("copurchase.png")
    print("✅ Saved: copurchase.png")


def plot_user(df, user_id):
    plt.figure()
    plt.bar(df["product"].astype(str), [1]*len(df))
    plt.title(f"🎯 Recommendations for User {user_id}")
    plt.xlabel("Product")
    plt.ylabel("Recommended")

    plt.savefig("user_recommendation.png")
    print("✅ Saved: user_recommendation.png")

# ---------------------------
# 🚀 MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":

    # Trending
    trending_df = get_trending()
    print(trending_df)
    plot_trending(trending_df)

    # Co-purchase
    copurchase_df = get_copurchase()
    print(copurchase_df)
    plot_copurchase(copurchase_df)

    # User recommendations
    user_id = int(input("Enter user id: "))
    user_df = get_user_recommendations(user_id)
    print(user_df)
    plot_user(user_df, user_id)
