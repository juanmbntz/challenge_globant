FROM python:3.8

# Add required libraries
RUN pip install requests
RUN pip install google-cloud-storage
RUN pip install json
RUN pip install google-cloud-bigquery
RUN pip install flask

# # Install Google Cloud SDK
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# # Add to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Add required scripts to the docker image
ADD utils.py .
ADD backfill.py .
ADD api_mail.py .
ADD start.sh .

# Add historic data files
ADD ./historic_backfill_data ./historic_backfill_data 

# Start bash script to run backfill and run API
CMD ["sh", "./start.sh"]

