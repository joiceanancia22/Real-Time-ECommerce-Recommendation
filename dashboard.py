import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 5 seconds
#st_autorefresh(interval=5000, key="refresh")

# ---------------------------
# TITLE
# ---------------------------
st.title("🛒 E-Commerce Recommendation Dashboard")

# ---------------------------
# NEO4J CONNECTION
# ---------------------------
driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "madhu0607")
)

# ---------------------------
# USER INPUT
# ---------------------------
user_id = st.number_input("Enter User ID", min_value=1)

# ---------------------------
# BUTTON
# ---------------------------
if st.button("Get Recommendations"):

    query = """
    MATCH (u:User {id: $uid})-[:BOUGHT]->(p1)-[:BOUGHT_WITH]->(p2)
    RETURN DISTINCT p2.id AS product
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query, uid=int(user_id))
        data = [r["product"] for r in result]

    df = pd.DataFrame(data, columns=["Recommended Products"])

    st.subheader("🎯 Recommended Products")
    st.write(df)

    if not df.empty:
        st.bar_chart(df.set_index("Recommended Products"))


