class Link
    # Линк к TORNADO
    # использует sockjs

    @connected: false
    @transport: false
    @callback_register: {}

    constructor: (@config) ->
        this.connect()

    # Создание соединения
    connect: ()->
        @transport = new SockJS('http://live_messages:9999/updater/')
        @transport.onopen = ()->
            window.link.connected()
        @transport.onclose = ()->
            window.link.disconnected()
        @transport.onmessage = ()->
            window.link.process_message()

    connected: ()->
        @connected = true

    disconnected: ()->
        @connected = false        

    
    process_message: ()->
        #Обработка сообщения
        console.log 'OPPPA'

    register: (callback, permanent) ->
        # Регистрируем функцию callback
        # Может быть перманентная - то есть на несколько вызовов
        # @param callback: function
        # @param permanent: bool


    query: (params, callback)->
        # Запрос 
        # @param params - Парметры запроса
        # @param callback - Функция обработчик (имя или функция)

        if typeof callback is 'function'
            callback_name = this.register callback, false
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