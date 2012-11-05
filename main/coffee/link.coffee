
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

    query: (tag, params, callback, method='get')->
        # Запрос 
        # @param params - Парметры запроса
        # @param callback - Функция обработчик (имя или функция)
        # @param tag - тег функции

        if typeof callback is 'function'
            @queues.register callback, tag

        data = {
            'params': params,
            'tags': [tag],
            'method': method
        }
        message = JSON.stringify data
        @transport.send message
    
    subscribe:(tag, callback) ->
        # Подписаться на сообщения по тегам
        @queues.register callback, tag

    post:(tag, data, callback) =>
        # Пост данных на сервер
        callback_ = (result) =>
            callback(result, data)
        @query tag, data, callback_, 'post'

    send_form: (form, callback) =>
        # Функция для отправки форм на сервер

        tag = form
        data = $(form).serializeArray()
        params = {}

        # @todo: Если параметры списком
        for row in data
            params[row['name']] = row['value']
        @query tag, params, callback

class Singleton
    constructor: (@record) ->
        @model = @record.constructor

Include = 
    ajax: -> new Singleton(this)
    
TransportModel = 
    # Расширение для моделей, что бы сохранять
    # и получать данные через линк

    extended: ->
        @change @transport_change
        # @include Include

    transport_change: (record, type, options) =>
        # Вызываем при изменении модели
        model = record.constructor.className.toLowerCase()
        if type is 'create'
            transport_link.post model, record, (data, post_data) =>
                if data?.id
                    record.changeID(data.id)
                    for field, value of data
                        if field != 'id'
                            record[field] = value
                    record.trigger('created',)

this.transport_link = new Link()
this.TransportModel = TransportModel