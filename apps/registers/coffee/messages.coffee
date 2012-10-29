
class Messages extends Spine.Controller
    # Сообщения
    @extend(Spine.Events)

    constructor: ->
        super
        @title = 'Журналы'
        @form = new MessagesForm({el: ".message-form"})
        @bind "enter", @on_show


    on_show: =>
        # Показываем основной контент
    

this.Messages = Messages