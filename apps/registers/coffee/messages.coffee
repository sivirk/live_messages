class Messages extends Spine.Controller
    # Сообщения
    @extend(Spine.Events)

    constructor: ->
        super
        @title = 'Журналы'
        @form = new MessagesForm({el: ".message-form"})

        $(".message-event").live "mouseover", (e) ->
            $(".message-actions",@).show()
        $(".message-event").live "mouseout", (e) ->
            $(".message-actions",@).hide()

        @bind "enter", @on_show
        @bind "update", @on_update

        Message.bind "created", (message)=>
            @insert message
        

    insert:(message...)=>
        # Добавляем новое сообщение
        templates.render_objects message..., (html) =>
            # Вставляем html после index сообщения
            $(".messages-list").prepend($(html))

    update: (params) =>
        # ...
        dairy_list  = $(".dairy-list")
        $("li", dairy_list).removeClass('active')
        $(".dairy__#{params.dairy}").addClass('active')
        if $(".dairy__#{params.dairy}").length
            @update_message_list()
    
    update_message_list: =>
        # Обновляем текуший список сообщений
        dairy = $(".dairy-list .active").attr("--data-id")
        params = {
            'register_id': dairy,
            'page': 1
        }
        transport_link.query 'message', params, (result) =>
            messages = (new Message(message) for message in result)
            @insert messages...

        

    on_update:(args...) =>
        # Обновление списка
        if args?.length
            params = args[0]
            @update params

    on_show: (args...) =>

        # Показываем основной контент
        if args?.length
            params = args[0]
            @update params

        dairy_list  = $(".dairy-list")
        if not $("li", dairy_list).length
            # Обновляем Журналы
            transport_link.query 'dairy', {}, (result) =>
                # Обновляем список всех журналов выбирая 1-ый
                url = null
                active = ''
                for dairy in result
                    dairy_name = dairy.slug
                    id = dairy.id
                    dairy_url = "/messages/#{dairy_name}/"
                    if not url
                        url = dairy_url
                    dairy = $("<li class='dairy__#{dairy_name} #{active}' --data-id='#{id}'><a href='##{dairy_url}'>" + dairy.title + "</a></li>")
                    dairy_list.append(dairy)
                @navigate url

this.Messages = Messages