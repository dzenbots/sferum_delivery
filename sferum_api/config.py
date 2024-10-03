from environs import Env

env = Env()
env.read_env()

vk_conversation_ids = env.list('VK_CONVERSATION_IDS')

client_remixdsid = env.str('REMIXDSID')

message_text = env.str('MESSAGE_TEXT')

start_delivery = env.str('START_DELIVERY')

lp_version = env.int('LP_VERSION')
v = env.str('V')
app_id = env.int('APP_ID')
