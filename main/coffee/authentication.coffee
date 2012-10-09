class Auth
    # Пользователь, вся информация об нем 
    # История

    constructor: () ->
        window.link.subscribe 'auth.error', @exception

    exception:(exception) ->
        console.log  exception['message']

    
    


$(document).ready ->
    window.auth = new Auth()