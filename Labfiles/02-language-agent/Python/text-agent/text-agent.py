from dotenv import load_dotenv
import os

# import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

import logging
import sys

# Enable debug logging for Azure SDK
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.DEBUG)

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
        agent_name = os.getenv('AGENT_NAME')
        
        # Get project client
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
            logging_enable=True # Added this parameter
        )
        
        
        
        # Get an OpenAI client
        openai_client = project_client.get_openai_client()
        

        
        # Use the agent to get a response
        # Use the agent to get a response
        prompt = input("User prompt: ")
        response = openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )

        print(f"{agent_name}: {response.output_text}")
        print(f"\nResponse Details: {response.model_dump_json(indent=2)}")
                
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()