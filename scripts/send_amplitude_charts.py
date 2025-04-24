#!/usr/bin/env python3
import os
import json
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def main():
    # 환경 변수에서 필요한 정보 가져오기
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    channel_id = os.environ.get('SLACK_CHANNEL_ID')
    
    if not slack_token:
        raise ValueError("SLACK_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
    
    if not channel_id:
        raise ValueError("SLACK_CHANNEL_ID 환경 변수가 설정되지 않았습니다.")
    
    # Slack 클라이언트 초기화
    client = WebClient(token=slack_token)
    
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
        # 헤더 메시지 보내기
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
        
        client.chat_postMessage(
            channel=channel_id,
            blocks=header_blocks,
            text=f"{today} Amplitude 일일 리포트"
        )
        
        # 각 차트마다 두 개의 메시지 보내기 (설명 + URL)
        for chart in amplitude_charts:
            # 설명이 포함된 메시지
            description_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{chart['title']}*\n{chart['description']}\n<{chart['url']}|차트 보기 👉>"
                    }
                }
            ]
            
            client.chat_postMessage(
                channel=channel_id,
                blocks=description_blocks,
                text=f"{chart['title']} - {chart['description']}"
            )
            
            # URL만 있는 메시지 - 차트가 렌더링되도록
            client.chat_postMessage(
                channel=channel_id,
                text=chart['url'],
                unfurl_links=True  # URL 미리보기 활성화
            )
            
        print("Amplitude 차트가 Slack으로 성공적으로 전송되었습니다.")
        
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    main()
