import os
from dotenv import load_dotenv

# import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential,get_bearer_token_provider


def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        token_provider=get_bearer_token_provider(DefaultAzureCredential(),"https://ai.azure.com/.default")  
        openai_client = OpenAI(base_url=azure_openai_endpoint, api_key=token_provider)

        #for previous link 
        last_response_id = None
        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response(by chat completion api)
            # completion=openai_client.chat.completions.create(
            #     model=model_deployment,
            #     messages=[
            #         {"role":"system",
            #          "content":"You are a helpful assistant that answers questions."},
            #         {"role":"user",
            #          "content":input_text}
            #     ]
            # )            
            # print(completion.choices[0].message.content)
            
            #no previous chat link
            #Modern way by response api
            # response=openai_client.responses.create(
            #     model=model_deployment,
            #     instructions="You are a helpful AI assistant that answers questions.",
            #     input=input_text
            # )
            # print(response.output_text)
            
            #with previous chat link
            response=openai_client.responses.create(
                model=model_deployment,
                instructions="You are a helpful AI assistant that answers questions.",
                input=input_text,
                previous_response_id=last_response_id
            )
            print(response.output_text)
            last_response_id = response.id

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
