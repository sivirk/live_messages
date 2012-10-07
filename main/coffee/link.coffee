
class QueueManager
    # Очереди обработчиков сообщений

    constructor: () ->    
        @cache = {}

    generate_name: () ->
        return 'opa'

    register: (callback, tags, limit) ->
        # Регистрируем функцию callback
        # Может быть перманентная - то есть на несколько вызовов
        # @param callback: function
        # @param permanent:

        tags = tags or this.generate_name()
        limit = limit or 1

        for tag in tags.split(",")
            if tag not in @cache
                this.cache[tag] = []
            this.cache[tag].push {"fnc": callback, "limit": limit}
        tags

    callback: (name, data) ->
        # Вызов функции обработчика с результатами
        # с сервера
        callbacks = @cache[name]
        if callbacks
            for callback in callbacks 
                callback['fnc'](data)
                if callback['limit']
                    callback['limit'] -= 1
                    if callback['limit'] == 0
                        delete @cache[name]
    
    

class Link
    # Линк к TORNADO
    # использует sockjs

    @connected: false
    @transport: false
    @reconnect: true
    @queues: false

    constructor: (@config) ->
        this.connect()
        @queues = new QueueManager()

    connect: ()->
        # Создание соединения
        @transport = new SockJS('http://live_messages:9999/transport/')
        @transport.onopen = ()->
            window.link.connected()
        @transport.onclose = ()->
            window.link.disconnected()
        @transport.onmessage = (e)->
            window.link.process_message(e)

    connected: ()->
        @connected = true

    disconnected: ()->
        @connected = false
        if @reconnect
            this.connect()

    process_message: (e)->
        #Обработка сообщения
        data = $.parseJSON e.data
        @queues.callback data['name'], data['result']

    query: (params, callback, is_blocking)->
        # Запрос 
        # @param params - Парметры запроса
        # @param callback - Функция обработчик (имя или функция)
        # @param block - Блокировать выполнение

        is_blocking = is_blocking or false

        if typeof callback is 'function'
            callback_name = @queues.register callback
        else
            callback_name = callback

        data = {
            'params': params,
            'name': callback_name
        }

        message = JSON.stringify data
        @transport.send message

$(document).ready ->
    window.link = new Link({})