""" Using Langchain Going to Generate a Server that can be used to shcedule meetings """
# Importing the required libraries
import langchain
import langchain_google_meet


# Create a Langchain LLM server.
server = langchain.Server()

# Create a Langchain Google Meet client.
client = langchain_google_meet.Client(server)
