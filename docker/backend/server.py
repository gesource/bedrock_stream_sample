import asyncio
import websockets
import boto3
import json
import os
from dotenv import load_dotenv
import logging

# 環境変数の読み込み
load_dotenv()

# ロギングの設定
logging.basicConfig(level=logging.INFO)

def get_aws_credentials():
    """AWSの認証情報を環境変数から取得する"""
    return {
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'region_name': os.getenv('AWS_REGION')
    }

async def invoke_bedrock(prompt: str):
    """Bedrock APIを非同期で呼び出す"""
    try:
        credentials = get_aws_credentials()
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            **credentials
        )
        body = json.dumps({
            'prompt': f"Human: {prompt}\nAssistant:",
            'temperature': 0.1,
            'top_p': 0.9,
            'max_tokens_to_sample': 300,
        })
        response = bedrock.invoke_model_with_response_stream(
            modelId='anthropic.claude-v2',
            accept='application/json',
            contentType='application/json',
            body=body
        )

        stream = response.get('body')
        if stream:
            for event in stream:
                chunk = event.get('chunk')
                if chunk:
                    decoded = json.loads(chunk.get('bytes').decode())
                    yield(decoded['completion'])
    except Exception as e:
        logging.error(f"Error during Bedrock API invocation: {e}")
        raise

async def echo(websocket, path):
    """WebSocket経由でメッセージを受信し、応答を返す"""
    async for message in websocket:
        logging.info(f"Received message: {message}")
        async for response in invoke_bedrock(message):
            logging.info(f"Sending response: {response}")
            await websocket.send(response)

async def main():
    """メイン関数でWebSocketサーバーを起動"""
    websocket_server = websockets.serve(echo, "0.0.0.0", 6789)
    async with websocket_server as server:
        logging.info("WebSocket server started.")
        await asyncio.Future()  # プログラムが終了しないようにする

# サーバーを起動
asyncio.run(main())
