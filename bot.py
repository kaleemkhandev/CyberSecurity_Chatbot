import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory, ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import json
import pickle
import base64

os.environ['OPENAI_API_KEY'] = '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'

# def return_response(txt_input:str):
#     llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)
#         # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
#     memory = ConversationBufferMemory()
#     # conversation_chain = ConversationalRetrievalChain.from_llm(
#     #     llm=llm,
#     #     retriever=db.as_retriever(),
#     #     memory=memory,
#     #     verbose=True
#     # )
#     prompt=PromptTemplate(input_variables=['history', 'input'], output_parser=None, partial_variables={},
#                         template='''You are a "Cyber Security Expert" who will answer the queries of "User", related to the
#                         field of Cyber Security. Strictly stay within the domain of Cyber Security and Do not answer any 
#                         questions which are outside the domain.
#                         Lets start." .\n\nCurrent conversation:\n{history}\n"User": {input}\n"Cyber Security Expert":''',
#                         template_format='f-string',
#                         validate_template=True)
#     conversation = ConversationChain(llm=llm, memory=memory, verbose=False, prompt=prompt)
#     response = conversation.predict(input=txt_input)
#     import pdb; pdb.set_trace()
#     return response
if __name__ == "__main__":
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
    # conversation_chain = ConversationalRetrievalChain.from_llm(
        #     llm=llm,
        #     retriever=db.as_retriever(),
        #     memory=memory,
        #     verbose=True
        # )
    
    # serialized_data_bytes = base64.b64decode(serialized_data_base64) #query db for serialized_data_base64
    # deserialized_data = pickle.loads(serialized_data_bytes)
    # memory = deserialized_data
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False, prompt=prompt)
    # print()
    while True:
        txt = input("Enter the Question: ")
        response = conversation.predict(input=txt)

        print("Bot:",response)
        # import pdb; pdb.set_trace()
        if txt == "1":
            break
        
        
    


