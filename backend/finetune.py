import openai
import os
import time
import json

def get_config_key():
    with open('../config.json') as f:
        config_data = json.load(f)
    return config_data["api_key"]

openai.api_key = get_config_key()



fine_tuning_job = openai.FineTuningJob.create(training_file="file-hh491O8PnZXGtAIKRFJhVXlM", validation_file="file-kQMWzSa067ptMsAdHqnuTSM2", model="gpt-3.5-turbo", hyperparameters={"n_epochs": 3})



job_id = fine_tuning_job["id"]
print(f"Fine-tuning job created with ID: {job_id}")

while True:
    print(openai.FineTuningJob.list_events(id=job_id, limit=10))
    

    time.sleep(60)
    