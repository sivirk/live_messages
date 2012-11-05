# Работа с шаблонами, при первом обращении грузится с бэкенда
# затем берется из кэша

class TemplateManager extends Spine.Controller

    constructor: ->
        super
        if localStorage
            @templates = localStorage
        else
            @templates = {}

    load_template:(template_name, callback) =>
        # Загружает нужный шаблон
        # вызывает callback с параметром - текст шаблона
        transport_link.query "templates", {'name': template_name}, (data) =>
            if data?.template
                @templates[template_name] = data.template
                callback(data.template)

    render_object: (object, callback)=>
        # Рендерит модель или список
        template = object.constructor.className.toLowerCase()
        template = "#{template}/client/read.html"
        return @render(template, object, callback)
    

    render: (template, context, callback) =>
        # Ренедрит шаблон с контекстом
        # @todo: Сделать протухание шаблонов
        if SETTINGS.debug or not @templates[template]
            @load_template template, (template) =>
                callback(Mustache.render(template, context))
        else
            template = @templates[template]
            callback(Mustache.render(template, context))

this.templates = new TemplateManager()