import os
import requests

edge_config_id = os.getenv('EDGE_CONFIG_ID')
team_id = os.getenv('TEAM_ID')
api_token = os.getenv('API_TOKEN')
url = f'https://api.vercel.com/v1/edge-config/{edge_config_id}/items'
params = {
    'teamId': team_id
}
headers = {
    'Authorization': f'Bearer {api_token}'
}

def get_prev_edge_stu(raw=0):
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    value = res.json()[0]['value']
    if raw:
        return value
    else:
        return [int(x) for x in value.split()]
        
def update_prev_edge_stu(new_content):
    # 입력값 검증
    items = new_content.strip().split()
    if len(items) != 14 or not all(x.isdigit() for x in items):
        raise Exception("previous_seat 값은 공백으로 구분된 14개의 정수여야 합니다.")
    
    body = {
        "items": [
            {
                "operation": "update",
                "key": "previous_seat",
                "value": new_content
            }
        ]
    }
    res = requests.patch(url, headers=headers, params=params, json=body)
    res.raise_for_status()
    return