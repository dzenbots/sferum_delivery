from sferum_api import config
from sferum_api.sferum_client import SferumClient


def main():
    client = SferumClient(config.client_remixdsid)
    client.authorize()
    # print(client.profile.access_token)
    for conversation in client.get_conversation_list():
        print(conversation)
    client.start_mail_distribution(
        message_text='Мое сообщение из моего бота для сферума',
        conversation_ids=config.vk_conversation_ids
    )


if __name__ == '__main__':
    main()
