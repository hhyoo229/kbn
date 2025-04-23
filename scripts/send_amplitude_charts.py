#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

def send_to_slack(webhook_url, message, blocks=None):
    """Slack webhook으로 메시지 전송"""
    slack_data = {
        "text": message
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
            "title": "일간 활성 사용자(DAU)",
            "url": "https://analytics.amplitude.com/your-org/chart/abc123",
            "description": "지난 24시간 동안의 활성 사용자 수"
        },
        {
            "title": "사용자 방문 경로",
            "url": "https://analytics.amplitude.com/your-org/chart/def456",
            "description": "주요 유입 경로 및 사용자 행동 분석"
        },
        {
            "title": "전환율 대시보드",
            "url": "https://analytics.amplitude.com/your-org/chart/ghi789",
            "description": "전환 단계별 이탈률 및 전환율"
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
