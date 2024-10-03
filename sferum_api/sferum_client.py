from dataclasses import dataclass
from random import randint
from typing import Union

import requests

from sferum_api import config


@dataclass
class SferumProfile:
    user_id: int
    profile_type: int
    access_token: str
    expires: int

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


@dataclass
class ServerCredentials:
    server: str
    key: str
    ts: int
    pts: int

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


@dataclass
class UserInfo:
    first_name: str
    last_name: str

    def __init__(self, conversation_info) -> None:
        self.first_name = conversation_info.get('first_name')
        self.last_name = conversation_info.get('first_name')


@dataclass
class GroupInfo:
    name: str
    photo_link: str

    def __init__(self, conversation_info) -> None:
        self.name = conversation_info.get('name')
        self.photo_link = conversation_info.get('photo_200')


@dataclass
class ChatInfo:
    title: str
    photo_link: str

    def __init__(self, conversation_info) -> None:
        self.title = conversation_info.get('title')
        self.photo_link = conversation_info.get('photo_base')


@dataclass
class Conversation:
    conversation_id: int
    conversation_type: str
    conversation_info: Union[UserInfo, GroupInfo, ChatInfo, None] = None

    def __init__(self, row_info: dict) -> None:
        self.conversation_id = row_info.get('peer').get('id')
        self.conversation_type = row_info.get('peer').get('type')


class SferumClient(requests.Session):
    client_remixdsid: str
    profile: SferumProfile
    credentials: ServerCredentials

    def __init__(self, client_remixdsid):
        super(SferumClient, self).__init__()
        self.client_remixdsid = client_remixdsid

    def authorize(self):
        req = self.get(
            url="https://web.vk.me/",
            params={
                "act": "web_token",
                "app_id": config.app_id
            },
            cookies={
                "remixdsid": self.client_remixdsid,
            },
            allow_redirects=False
        )
        self.profile = SferumProfile(**req.json()[1])
        req = self.post(
            url="https://api.vk.me/method/messages.getLongPollServer",
            params={
                "v": config.v
            },
            data={
                "need_pts": 1,
                "group_id": 0,
                "lp_version": config.lp_version,
                "access_token": self.profile.access_token
            }
        )
        self.credentials = ServerCredentials(**req.json()["response"])

    def get_user_info(self, user_id: int) -> Union[dict, None]:
        pass

    def get_conversation_list(self) -> list[Conversation]:
        req = self.post(
            url="https://api.vk.me/method/messages.getConversations",
            params={
                "v": config.v
            },
            data={
                "access_token": self.profile.access_token,
            }
        )
        conversations = []
        for conversation in req.json().get('response').get('items'):
            new_conversation = Conversation(conversation.get('conversation'))
            if new_conversation.conversation_type == 'chat':
                new_conversation.conversation_info = ChatInfo(
                    conversation_info=conversation.get('conversation').get('chat_settings')
                )
            if new_conversation.conversation_type == 'user':
                new_conversation.conversation_info = UserInfo(
                    conversation_info=self.post(
                        url="https://api.vk.me/method/users.get",
                        params={
                            "v": config.v
                        },
                        data={
                            "access_token": self.profile.access_token,
                            'user_ids': new_conversation.conversation_id
                        }
                    ).json()['response'][0]
                )
            if new_conversation.conversation_type == 'group':
                new_conversation.conversation_info = GroupInfo(
                    conversation_info=self.post(
                        url="https://api.vk.me/method/groups.getById",
                        params={
                            "v": config.v
                        },
                        data={
                            "access_token": self.profile.access_token,
                            'group_ids': abs(new_conversation.conversation_id)
                        }
                    ).json()['response'].get('groups')[0]
                )
            conversations.append(new_conversation)
        return conversations

    def start_mail_distribution(self, message_text: str, conversation_ids):
        for id in conversation_ids:
            print(f'Отправляю сообщение в чат с id={id}')
            self.send_message(id=abs(id), message_text=message_text)

    def send_message(self, id: int, message_text: str):
        req = self.post(
            url="https://api.vk.me/method/messages.send",
            params={
                "v": config.v
            },
            data={
                "access_token": self.profile.access_token,
                "peer_id": id,
                "random_id": -randint(100000000, 999999999),
                "message": message_text
            }
        )