class Auth extends Spine.Controller
    @extend(Spine.Events)

    # events:
        # "click .auth-btn": "on_auth_btn_click"

    constructor: (config) ->
        super
        @title = 'Авторизация'
        @user = config.user
        @bind "enter", @on_show
        # на показ новой вьюхи
        # 1 - биндим обновление поля userinfo
        @bind "new_view", @updateUserInfo

        $(".auth-btn").on('click', @login)
        $(".auth-logout").on('click', @logout)
        transport_link.subscribe 'auth.error', @go_authentificate

    is_authentificated: =>
        # ...
        if @user?.user_id
            return true
        else
            false
    
    on_show: =>
        if @user_id
            @navigate application.next_url()

    
    updateUserInfo: (view) =>
        if view == 'messages'
            user_info = $(".user-info > span")

        if @user.user_name
            user_info.html(@user.user_name)
        

    go_authentificate:(exception) ->
        # Исключение возникающее в случае 
        # проблем с авторизацией или аутентификацией

    login: (e)=>
        # Авторизация

        transport_link.send_form ".login-form form", (result) =>
            # Обрабатываем ответ авторизации
            if result.success
                @user = result.user
                @trigger "exit"
            else
                
        return false

    logout:(e) =>
        # Выход
        transport_link.query "logout", {}, (result) =>
                # Обрабатываем ответ авторизации
                if result.success
                    @user = null
                    @trigger 'authentification_required'
                
        return false
    

this.Auth = Auth