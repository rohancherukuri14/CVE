import openai
import os
import time
import json

def get_config_key():
    with open('../config.json') as f:
        config_data = json.load(f)
    return config_data["api_key"]

openai.api_key = get_config_key()

# output_file = openai.File.create(
#   file=open("output.jsonl", "rb"),
#   purpose='fine-tune'
# )

# validation_file = openai.File.create(
#   file=open("validation.jsonl", "rb"),
#   purpose='fine-tune'
# )

# print(output_file)
# print(validation_file)


# fine_tuning_job = openai.FineTuningJob.create(training_file="file-yK4Bud6AexdiBgmMxQIVGagG", validation_file="file-AyQPUwx50s4semQ5qk9yxqO6", model="gpt-3.5-turbo")



# job_id = fine_tuning_job["id"]
# print(f"Fine-tuning job created with ID: {job_id}")

    
print(openai.FineTuningJob.retrieve("ftjob-iYgJHNJKlgIn8ypelpoJMK1U"))
print(openai.FineTuningJob.list_events(id="ftjob-iYgJHNJKlgIn8ypelpoJMK1U", limit=10))