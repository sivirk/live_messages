
# Автокомплит для сообщений
OBJECT_TRIGGER = "#";
triggered = false
focus = false

SIMPLE_ELEMENTS = ["ActionScript","AppleScript","Asp","BASIC","C","C++","Clojure","COBOL","ColdFusion","Erlang","Fortran","Groovy","Haskell","Java","JavaScript","Lisp","Perl","PHP","Python","Ruby","Scala","Scheme"];

$(document).ready ->
    $("#new_message").autocomplete
        source: SIMPLE_ELEMENTS
        # minLength: 0
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