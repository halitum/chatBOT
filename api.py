from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from back import get_spark
from config import default_init_history
import database as db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许所有ip跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 接收POST请求中的数据
class Item(BaseModel):
    prompt : str
    groupId : int   # qq群号
    name : str      # 发送信息者用户名
    userId : int    # qq号

class Init_Config(BaseModel):
    temperature : str = 0.8
    top_k : str = 4
    max_history_lenth : str = 20

class Message(BaseModel):
    role: str
    content: str

class Init_History(BaseModel):
    init_history: List[Message]

@app.post("/spark/")
async def get_spark_response(item: Item):
    '''
    聊天功能实现
    '''
    response = get_spark(item)
    print("name:", item.name, "\n", "response:", response)
    return response

@app.get("/dash/")
async def get_user_info(id: int):
    '''
    获取用户面板信息
    '''
    response = db.read_config(id)
    return response

@app.get("/dash/type/")
async def get_init_history_type(id: int):
    '''
    获取长期记忆设定类型
    '''
    response = db.get_memory_set(id)
    return response

@app.delete("/dash/")
async def reset_conversation(id: int):
    '''
    重置当前对话
    '''
    db.reset_conversation_history(id)
    return 200

@app.post("/dash/")
async def reset_default_congfig(id: int):
    '''
    恢复默认设置
    '''
    db.reset_default_congfig(id)
    return 200
    
@app.get("/dash/login/")
async def log_in(id: int):
    '''
    返回用户名
    '''
    return db.read_user_name(id)

@app.post("/dash/edit_history/")
async def edit_history(id: int, init_history: Init_History):
    '''
    编辑长期历史配置
    '''
    db.edit_init_history(id, init_history)
    return 200

@app.post("/dash/edit_config/")
async def edit_config(id: int, init_config: Init_Config):
    '''
    编辑其他LLM配置
    '''
    db.edit_other_config(id, init_config)
    return 200

# # 测试POST接收前端数据
# @app.post("/test/")
# async def receive_data(request: Request):
#     # 接收请求数据
#     data = await request.body()
#     data_str = data.decode('utf-8')
    
#     try:
#         data_json = json.loads(data_str)
#         print("Received JSON data:", data_json)
#     except json.JSONDecodeError:
#         print("Received data is not in JSON format:", data_str)
    
#     return {"status": "Data received", "data": data_str}