import json
import asyncio
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

        # 모델 응답을 스트리밍으로 처리
        await self.llm_response(user_message)

    async def llm_response(self, user_message):
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
        chain = model | StrOutputParser()

        # 동기적인 stream 함수는 asyncio.to_thread로 처리
        response_generator = await asyncio.to_thread(chain.stream, user_message)

        # 스트리밍 응답을 처리하는 비동기 함수
        for chunk in response_generator:
            # 스트리밍 데이터를 실시간으로 웹소켓을 통해 전송
            await self.send(text_data=json.dumps({
                'response': chunk
            }))
