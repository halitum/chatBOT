# 不可供用户调整调的大模型参数
MAX_TOKEN = 384

# 默认模型参数
msg = {
    'sys':'',
    'user1':'',
    'ass1':'',
    'user2':'',
    'ass2':'',
    'user3':'',
    'ass3':'',
}

default_init_history = [{
    'role': 'system',
    'content': msg['sys'],
},{
    'role': 'user',
    'content': msg['user1'],
},{
    'role': 'assistant',
    'content': msg['ass1'],
},{
    'role': 'user',
    'content': msg['user2'],
},{
    'role': 'assistant',
    'content': msg['ass2'],
},{
    'role': 'user',
    'content': msg['user3'],
},{
    'role': 'assistant',
    'content': msg['ass3'],
}]

default_init_config = [
    {   
        'init_history': default_init_history,
        'temperature': '0.8',
        'top_k': '4',
        'max_history_lenth': '20'
    }
]


acnt = {
    'SPARKAI_APP_ID': "",
    'SPARKAI_API_SECRET': "",
    'SPARKAI_API_KEY': "",
    'SPARKAI_DOMAIN': "",
    'SPARKAI_URL': "",
}

# db = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': '',
#     'db': 'chatbot'
# }

db = r''
