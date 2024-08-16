FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY consistency_prompt /app/consistency_prompt
COPY Event_graph /app/Event_graph
COPY Anomaly_detect.py /app/Anomaly_detect.py
COPY data_constraints.json /app/data_constraints.json
COPY commonsense_constraints.json /app/commonsense_constraints.json
COPY trigger_constraints.json /app/trigger_constraints.json
COPY Train_data.txt /app/Train_data.txt
COPY Test_data.txt /app/Test_data.txt
COPY Test_data_modify.txt /app/Test_data_modify.txt
COPY dataflow.log /app/dataflow.log
COPY slimit /usr/local/lib/python3.10/site-packages/slimit

CMD ["bash"]
