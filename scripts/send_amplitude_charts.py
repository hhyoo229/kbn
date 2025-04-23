#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

def send_to_slack(webhook_url, message, blocks=None):
    """Slack webhook으로 메시지 전송"""
    slack_data = {
        "text": message,
        "unfurl_links": True
    }
    
    if blocks:
        slack_data["blocks"] = blocks
    
    response = requests.post(
        webhook_url, 
        data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        raise ValueError(f"Slack API 요청 실패: {response.status_code}, {response.text}")
    
    return response

def main():
    # 환경 변수에서 Slack Webhook URL 가져오기
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
    
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
    
    # Slack에 보낼 블록 메시지 구성
    blocks = [
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
    
    # 각 차트에 대한 섹션 추가
    for chart in amplitude_charts:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{chart['title']}*\n{chart['description']}\n<{chart['url']}|차트 보기 👉>\n{chart['url']}"
            }
        })
        blocks.append({
            "type": "divider"
        })
    
    # 메시지 전송
    send_to_slack(
        webhook_url,
        f"{today} Amplitude 일일 리포트",
        blocks
    )
    print("Amplitude 차트가 Slack으로 성공적으로 전송되었습니다.")

if __name__ == "__main__":
    main()
