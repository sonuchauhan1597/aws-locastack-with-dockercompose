FROM python:3.6
RUN pip install boto3 awscli && mkdir -p /opt 
WORKDIR /opt
COPY generator.py /opt/generator.py
COPY create_dydb.py /opt/create_dydb.py
COPY sqs_message_ops.py /opt/sqs_message_ops.py
CMD /bin/sh

