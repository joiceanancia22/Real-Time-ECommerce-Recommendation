FROM python:3.10

WORKDIR /app
COPY . /app

# Install Java (lightweight)
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
    apt-get update --fix-missing && \
    apt-get install -y default-jre && \
    rm -rf /var/lib/apt/lists/*

# SET JAVA PATH (CRITICAL)
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

# Install dependencies
RUN pip install pandas neo4j matplotlib streamlit streamlit-autorefresh
RUN pip install pyspark==3.5.1

CMD ["python", "spark_jobs/stream_processor.py"]
