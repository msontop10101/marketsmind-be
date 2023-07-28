from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.llms import OpenAI
from langchain import LLMChain
import os

# Initialize the LLMChain with the environment variable
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
template = "You're a finance chatbot that answers people's question relating only to finance. Your range of topic and expertise goes from crypto, stocks, defi, forex and commodities."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt_preset = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
llm_chain = LLMChain(prompt=chat_prompt_preset, llm=llm)


@api_view(['POST'])
def answer_question(request):
    if request.method == 'POST':
        # Get the user's message from the request data
        user_message = request.data.get('message', '')
        if user_message:
            # Get the response from the LLMChain
            response = llm_chain.run(user_message)
            return Response({'response': response})
        else:
            return Response({'error': 'No message provided'}, status=400)
