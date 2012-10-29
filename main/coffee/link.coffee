
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
    
    

class Link extends Spine.Controller
    # Линк к серверу transport
    # использует sockjs

    @connected: false
    @transport: false
    @reconnect: true
    @queues: false

    constructor: (@config) ->
        @config = SETTINGS.transport
        @connect()
        @queues = new QueueManager()
        @reconnect = true

    connect: ()->
        # Создание соединения
        address = @config.address
        port = @config.port

        @transport = new SockJS("http://#{ address }:#{ port }/transport/")
        @transport.onopen = ()=>
            @on_connected()
        @transport.onclose = ()=>
            @on_disconnected()
        @transport.onmessage = (e)=>
            @process_message(e)

    on_connected: ()=>
        @connected = true

    on_disconnected: ()=>
        @connected = false
        if @reconnect
            @transport = false
            @connect()

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

    send_form: (form, callback) =>
        # Функция для отправки форм на сервер

        tag = form
        data = $(form).serializeArray()
        params = {}

        # @todo: Если параметры списком
        for row in data
            params[row['name']] = row['value']
        @query tag, params, callback
    
    

this.transport_link = new Link()