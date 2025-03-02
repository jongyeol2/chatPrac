import json
from channels.generic.websocket import AsyncWebsocketConsumer
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data['message']
        
        llm_response = await self.llm_response(user_message)
        
        await self.send(text_data=json.dumps({
            'response': llm_response
        }))
    
    async def llm_response(self, user_message):
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        chain = model | StrOutputParser()
        
        response = chain.invoke(user_message)
        return response
