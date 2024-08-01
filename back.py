from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import database as db
from config import acnt, default_init_history, MAX_TOKEN

def get_spark(item):
    # in_group：是否在群聊中
    in_group = True if(item.groupId != item.userId) else False
    
    # 工具函数：传入初始对话与用户对话，并将[{},{}...]转换成[chatMessage(),chatMessage(),...]
    def convert_dict_to_chatMessage(history):
        conversation_history = []

        for text in history:
            for message in text:
                conversation_history.append(ChatMessage(
                    role=message['role'],
                    content=message['content']
                ),)

        return conversation_history

    # 功能函数：调用大模型api
    def get_respond(id):

        if not db.read_config(id):
            name = f"群{item.groupId}管理员" if in_group else f"{item.name}"
            db.create_user(id, name)
        
        config = db.read_config(id)[0]
        spark = ChatSparkLLM(
            spark_api_url=acnt['SPARKAI_URL'],
            spark_app_id=acnt['SPARKAI_APP_ID'],
            spark_api_key=acnt['SPARKAI_API_KEY'],
            spark_api_secret=acnt['SPARKAI_API_SECRET'],
            spark_llm_domain=acnt['SPARKAI_DOMAIN'],
            temperature=float(config['temperature']),
            top_k=int(config['top_k']),
            max_tokens=MAX_TOKEN,
            streaming=False,
        )

        db.update_conversation_history(id, {'role':'user', 'content':item.prompt}, int(config['max_history_lenth']), len(config['init_history']))
        conversation_history = convert_dict_to_chatMessage([
                                                config['init_history'],
                                                db.read_conversation_history(id)
                                                ]
                                            )

        handler = ChunkPrintHandler()
        # 生成回复
        respond = spark.generate([conversation_history], callbacks=[handler])
        res = respond.generations[0][0].text
        
        db.update_conversation_history(id, {'role':'assistant', 'content':res}, int(config['max_history_lenth']), len(config['init_history']))

        return res
    
    # INFO命令实现
    def check_info(id):
        config = db.read_config(id)[0]
        history = db.read_conversation_history(id)
        conversation_lenth = len(history) if history else 0
        memory_set = db.get_memory_set(id)
        res = f"当前对话长度：{conversation_lenth}\n最大可记忆对话长度：{config['max_history_lenth']}\n长期记忆设定：{memory_set}\nTemperature：{config['temperature']}\nTop_k采样数：{config['top_k']}"
        return res

    # get_spark函数主函数：优先执行BOT指令(若存在)，否则返回大模型信息
    def main():
        if "RESET" in str(item.prompt):
            db.reset_conversation_history(item.groupId if in_group else item.userId)
            res = "<历史会话已清除>"
        elif "INFO" in str(item.prompt):
            res = check_info(item.groupId if in_group else item.userId)
        else:
            res = get_respond(item.groupId)

        if in_group:
            return "<公共频道>\n"+res
        return res
    
    return main()