
class QueueManager
    # Очереди обработчиков сообщений

    constructor: () ->    
        @cache = {}

    register: (callback, tags, limit) ->
        # Регистрируем функцию callback
        # Может быть перманентная - то есть на несколько вызовов
        # @param callback: function
        # @param permanent:

        tags = tags
        limit = limit or 1

        for tag in tags.split(",")
            if tag not in @cache
                this.cache[tag] = []
            this.cache[tag].push {"fnc": callback, "limit": limit}

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
        config = SETTINGS.transport
        this.connect config.address, config.port
        @queues = new QueueManager()
        @reconnect = false

    connect: (address, port)->
        # Создание соединения
        @transport = new SockJS("http://#{ address }:#{ port }/transport/")
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
        for tag, tag_data of data
            @queues.callback tag, tag_data

    query: (tag, params, callback)->
        # Запрос 
        # @param params - Парметры запроса
        # @param callback - Функция обработчик (имя или функция)
        # @param tag - тег функции

        is_blocking = is_blocking or false

        if typeof callback is 'function'
            @queues.register callback, tag

        data = {
            'params': params,
            'tags': [tag]
        }
        message = JSON.stringify data
        @transport.send message
    
    subscribe:(tag, callback) ->
        # Подписаться на сообщения по тегам
        @queues.register callback, tag


APPS?.Link = Link