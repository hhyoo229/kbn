#!/usr/bin/env python3
import os
import json
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def main():
    # 환경 변수에서 필요한 정보 가져오기
    bot_token = os.environ.get('SLACK_BOT_TOKEN')
    user_token = os.environ.get('SLACK_USER_TOKEN')  # 사용자 토큰 추가
    channel_id = os.environ.get('SLACK_CHANNEL_ID')
    
    if not bot_token:
        raise ValueError("SLACK_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
    
    if not user_token:
        raise ValueError("SLACK_USER_TOKEN 환경 변수가 설정되지 않았습니다.")
    
    if not channel_id:
        raise ValueError("SLACK_CHANNEL_ID 환경 변수가 설정되지 않았습니다.")
    
    # Bot 클라이언트와 User 클라이언트 초기화
    bot_client = WebClient(token=bot_token)
    user_client = WebClient(token=user_token)
    
    # 오늘 날짜 가져오기
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    # Amplitude 차트 URL 목록
    amplitude_charts = [
        {
            "title": "일일 로그인 에러 차트",
            "url": "https://app.amplitude.com/analytics/smilegatestove/chart/7upn1ag7",
            "description": "지난 일주일간 로그인 에러코드별 카운트 추이"
        }
    ]
    
    try:
        # 헤더 메시지 보내기 (봇으로 전송)
        header_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 {today} Amplitude 일일 리포트",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            }
        ]
        
        bot_client.chat_postMessage(
            channel=channel_id,
            blocks=header_blocks,
            text=f"{today} Amplitude 일일 리포트"
        )
        
        # 각 차트에 대한 설명 메시지는 봇으로 전송
        for chart in amplitude_charts:
            description_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{chart['title']}*\n{chart['description']}\n<{chart['url']}|차트를 보려면 아래 URL을 확인하세요>"
                    }
                }
            ]
            
            bot_client.chat_postMessage(
                channel=channel_id,
                blocks=description_blocks,
                text=f"{chart['title']} - {chart['description']}"
            )
            
            # URL만 있는 메시지는 사용자 계정으로 전송
            user_client.chat_postMessage(
                channel=channel_id,
                text=chart['url']
            )
            
        print("Amplitude 차트가 Slack으로 성공적으로 전송되었습니다.")
        
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    main()
