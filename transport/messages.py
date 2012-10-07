# -*- coding: UTF-8 -*-

import json


class MessageManager(object):
    """ Обработка входящих сообщений
        от клиента
    """

    def __init__(self,):
        pass

    def handle_message(self, client, message,):
        data = json.loads(message)
        result = {'name': data['name']}
        result['result'] = ['PYTHON', "FIGON", "GOPA"]
        return json.dumps(result)
