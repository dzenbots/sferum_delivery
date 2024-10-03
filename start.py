from sferum_api import config
from sferum_api.sferum_client import SferumClient


def main():
    client = SferumClient(config.client_remixdsid)
    client.authorize()
    for conversation in client.get_conversation_list():
        print(conversation)
    if config.start_delivery:
        client.start_mail_distribution(
            message_text=config.message_text,
            conversation_ids=config.vk_conversation_ids
        )


if __name__ == '__main__':
    main()
