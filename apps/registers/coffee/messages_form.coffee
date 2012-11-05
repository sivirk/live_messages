
# Автокомплит для сообщений
OBJECT_TRIGGER = "#";
triggered = false
focus = false

class MessagesForm extends Spine.Controller

    events:
        "click .message-type": "change_type"
        "click .save-btn": "save"
        "click .tags .add": "add_tags"

    constructor: ->
        super
        @start_autocomplete()

    add_tags:(e) =>
        # ...

    

    save:(e) ->
        # Добавление - сохранение сообщения
        text = $(".message").val()
        if text
            purpose = $(".type-pointed").attr("class").split(" ")[3]
            tags = $(".tags .tag").map (e) ->
                $(this).attr("--data-tag")
            tags = tags.get()
            # if purpose in ["event", "announce"]
            message = new Message(
                    text: text
                    purpose: purpose
                    tags: tags
            )
            message.save()

    change_type: (e) ->
        # Смена типа сообщения
        # Показывается/скрывается поле даты
        message_type = $(e.target)
        pointed = message_type.hasClass('type-pointed')
        if not pointed
            $(".message-type").removeClass("type-pointed")
            $(".message-pointer").removeClass("pointed")
            message_type.addClass("type-pointed")
            position = message_type.attr('class').split(" ")[1]
            $(".type-pointers>.#{position}").addClass("pointed")
            if message_type.attr('class').indexOf("info") != -1
                if $(".submenu").css("display") == 'block'
                    $(".submenu").effect("drop", {}, 50)
            else
                if $(".submenu").css("display") != 'block'
                    $(".submenu").effect("slide", {}, 50)

    start_autocomplete: ->
        # Стартуем автокомлит сообщений
        $(".message").autocomplete
            source: (request, response) ->
                query_params = {'request': request.term}
                transport_link.query 'autocomplete', query_params, response
            search: () ->
                return false if not triggered
            select: (event, ui) ->
                text = this.value
                pos = text.lastIndexOf(OBJECT_TRIGGER)
                this.value = text.substring(0, pos) + ' ' + OBJECT_TRIGGER + ui.item.value
                triggered = false
                focus = false
                return false
            focus: (event, ui) ->
                focus = this.value
                event.preventDefault()
                return true
        .bind 'keyup', () ->
            if not focus
                text = this.value
                len = text.length
                if triggered
                    index = text.lastIndexOf(OBJECT_TRIGGER)
                    query = text.substring(index + OBJECT_TRIGGER.length)
                    $(this).autocomplete("search", query)
                else                 
                    last = text.substring(len - OBJECT_TRIGGER.length)
                    triggered = (last == OBJECT_TRIGGER)
    
this.MessagesForm = MessagesForm
