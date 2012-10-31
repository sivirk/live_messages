class Application extends Spine.Controller 

    @currentview

    constructor: (config) ->
        super
        @views = {
                'auth' : new Auth({
                    'el': $(".auth_form"),
                    'user': config.user
                })
                'messages' : new Messages({'el': $(".content")})
            }
        @views['auth'].bind "authentification_required", (args...) =>
            @navigate "/login/"
            # @show_controller 'auth', {'redirect': location.hash}

        # Основные - root - урлы
        @routes
            # Сообщения
            "/messages/:dairy/": (params) =>
                @show_controller 'messages', {''}, params
            "/messages/": =>
                @show_controller 'messages'
            # Авторизация
            "/login/": =>
                @show_controller 'auth', {'redirect': location.hash}
        Spine.Route.setup()
        # Проверяем аутентифицирован ли пользователь и показываем
        # основной контент - сообщения
        if @views['auth'].is_authentificated()
            if not location.hash
                @navigate "/messages/"
            else
                @navigate "/gopa/"
        else
            @navigate "/login/"

    next_url:=>
        return "/messages/"
    

    show_controller:(screen='messages', options={}, args...) =>
        # Меняем экран вызывая соответствующий view
        # @TODO: Переход между вьюхами, анимация

        if typeof screen is 'string'
            screen = @views[screen]
        
        $(".open").removeClass("open")

        # Меняем текущую вьюху на новую
        if @currentview != screen
            show_effect = false
            if @currentview
                @currentview.unbind 'exit'
                @currentview.el.effect('slide',{'direction':'right', 'mode':'hide'})
                @currentview.el.hide()
                show_effect = true
            @currentview = screen
            for view_name, view of @views
                if view == @currentview
                    currentview_name = view_name
            document.title = screen.title
            if show_effect
                screen.el.show()
            else
                screen.el.show()

            screen.trigger "enter", args...
            # Уведомляем другие контролы что показана вьюха
            for view_name, view of @views
                if view != @currentview
                    view.trigger "new_view", currentview_name

            # Определяем что делать на выход из вьюхи
            if options.redirect
                screen.bind "exit", (args) =>
                    # После выхода из вьюхи редиректим на указанный урл
                    @navigate options.redirect
            else
                screen.bind "exit", (action, args...) =>
                    # Либо проверяем параметры, если это название 
                    # то показываем соответствующий view
                    # или редиректим на указанный урл
                    if action?.indexOf "/" == 0
                        @navigate action
                    else if action
                        @show_controller action
                    else
                        @navigate "/messages/"
        else
            screen.trigger "update", args...
            
this.Application  = Application