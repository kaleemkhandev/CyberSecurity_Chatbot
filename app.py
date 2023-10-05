# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory, ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# MongoDB Cluster URL :

#insert
# db.insert_one({"user_id":"abc123","qna":[[1,2]]})
#find specific user based on his user id
# print("---- BEFOR -------", db.find_one({"user_id":"abc123"}))
#updating an exixting users' qna
# print("-------- AFTER ------" , db.find_one_and_update({"user_id":"abc123"} , {"$set":{ "qna":[[2,3] , ["a" , "b"]]}}))
# Again get updated
# print("---- AFTER FIND -------", db.find_one({"user_id":"abc123"}))
# db.delete_one({"user_id":"abc123"})
def load_history(QnA:list):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)
            # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferWindowMemory(k=10)
    prompt=PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={},
                                template='''You are a "Cyber Security Expert" who will answer the queries of "User", related to the
                                field of Cyber Security. Strictly stay within the domain of Cyber Security and Do not answer any 
                                questions which are outside the domain. 
                                Always keep the answers precise and to the point.
                                Lets start." .\n\nCurrent conversation:\n{history}\n"User": {input}\n"Cyber Security Expert":''',
                                template_format='f-string',
                                validate_template=True)
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False, prompt=prompt)


    for qna in QnA:
        question,answer = qna[0],qna[1]
        conversation.memory.chat_memory.messages.append(HumanMessage(content = question,additional_kwargs={},example=False))
        conversation.memory.chat_memory.messages.append(AIMessage(content= answer,additional_kwargs={},example=False))
    
    return conversation
    



def return_first_response(input_text):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)
            # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferWindowMemory(k=10)
    prompt=PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={},
                                template='''You are a "Cyber Security Expert" who will answer the queries of "User", related to the
                                field of Cyber Security. Strictly stay within the domain of Cyber Security and Do not answer any 
                                questions which are outside the domain.
                                Lets start." .\n\nCurrent conversation:\n{history}\n"User": {input}\n"Cyber Security Expert":''',
                                template_format='f-string',
                                validate_template=True)
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False, prompt=prompt)
    response = conversation.predict(input=input_text)
    return response

def return_response(input_text:str,QnA:list):
    conversation = load_history(QnA)
    response = conversation.predict(input=input_text)
    return response    
