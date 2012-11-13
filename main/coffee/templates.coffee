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

    render_objects: (objects..., callback)=>
        # Рендерит модель или список
        object_name = objects[0].constructor.className.toLowerCase()
        is_objects_same = (o.constructor.className.toLowerCase()==object_name for o in objects).reduce (f,n)=> f&&n
        if is_objects_same
            template = "#{object_name}/client/read.html"
            return @render(template, {'objects': objects}, callback)
    

    render: (template, context, callback) =>
        # Ренедрит шаблон с контекстом
        # @todo: Сделать протухание шаблонов
        if SETTINGS.debug or not @templates[template]
            @load_template template, (template) =>
                if context.objects
                    (callback(Mustache.render(template, o)) for o in context.objects)
                else
                    callback(Mustache.render(template, context))
        else
            template = @templates[template]
            if context.objects
                (callback(Mustache.render(template, o)) for o in context.objects)
            else
                callback(Mustache.render(template, context))

this.templates = new TemplateManager()