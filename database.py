# import pymysql
import sqlite3
from config import db, default_init_config, default_init_history
import json

# # 连接到 MySQL 数据库
# def create_connection():
#     connection = None
#     try:
#         connection = pymysql.connect(**db)
#     except pymysql.MySQLError as e:
#         print(f"Error: '{e}'")
#     return connection

# 连接到 SQLite 数据库
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(db)
    except sqlite3.Error as e:
        print(f"Error: '{e}'")
    return connection

# 创建用户
def create_user(user_id, user_name):
    connection = create_connection()
    cursor = connection.cursor()
    config_json = json.dumps(default_init_config)
    query = "INSERT INTO ConversationHistory (id, config, name) VALUES (?, ?, ?)"
    values = (user_id, config_json, user_name)
    cursor.execute(query, values)
    connection.commit()
    connection.close()

# 读取用户名
def read_user_name(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT name FROM ConversationHistory WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()

    if result:
        return result
    else:
        return None

# 读取长期记忆类型
def get_memory_set(user_id):
    config = read_config(user_id)[0]
    memory_set = 'default' if config['init_history'] == default_init_history else 'Customize'
    return memory_set

# 更新对话记录
def update_conversation_history(user_id, new_message, MAX_HISTORY_LENGTH, init_len):
    connection = create_connection()
    cursor = connection.cursor()
    # 读取当前的历史记录
    query = "SELECT history FROM ConversationHistory WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result[0]:
        history = json.loads(result[0])
    else:
        history = []
    # 添加新的对话记录
    history.append(new_message)

    # 检查并维护会话历史长度
    while len(history) > (MAX_HISTORY_LENGTH + init_len):
        history.pop(0)

    history_json = json.dumps(history)
    # 更新历史记录
    update_query = "UPDATE ConversationHistory SET history = ? WHERE id = ?"
    cursor.execute(update_query, (history_json, user_id))
    connection.commit()
    connection.close()

# 读取系统设置
def read_config(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT config FROM ConversationHistory WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()
    
    # 检查id是否存在
    if result:
        config = json.loads(result[0])
        return config
    else:
        return False
    
# 读取历史对话
def read_conversation_history(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT history FROM ConversationHistory WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    connection.close()

    # 检查history单元格是否被填充了Null（如果是，result返回的是(None,)）
    if result[0]:
        history = json.loads(result[0])
        return history
    else:
        return None
    
# 重置历史对话
def reset_conversation_history(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    update_query = "UPDATE ConversationHistory SET history = NULL WHERE id = ?"
    cursor.execute(update_query, (user_id,))
    connection.commit()
    connection.close()

# 删除用户信息
def delete_user(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM ConversationHistory WHERE id = ?"
    cursor.execute(delete_query, (user_id,))
    connection.commit()
    connection.close()

# 将init_config设置为默认值
def reset_default_congfig(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    config_json = json.dumps(default_init_config)
    update_query = "UPDATE ConversationHistory SET config = ? WHERE id = ?"
    cursor.execute(update_query, (config_json, user_id))
    connection.commit()
    connection.close()

def edit_init_history(user_id, new_history):
    connection = create_connection()
    cursor = connection.cursor()
    config = read_config(user_id)
    config[0]['init_history'] = [message.dict() for message in new_history.init_history]
    config = json.dumps(config)
    update_query = "UPDATE ConversationHistory SET config = ? WHERE id = ?"
    cursor.execute(update_query, (config, user_id))
    connection.commit()
    connection.close()

def edit_other_config(user_id, new_config):
    connection = create_connection()
    cursor = connection.cursor()
    config = read_config(user_id)
    config[0]['temperature'] = new_config.temperature
    config[0]['top_k'] = new_config.top_k
    config[0]['max_history_lenth'] = new_config.max_history_lenth
    config = json.dumps(config)
    update_query = "UPDATE ConversationHistory SET config = ? WHERE id = ?"
    cursor.execute(update_query, (config, user_id))
    connection.commit()
    connection.close()