// Generated by CoffeeScript 1.3.3
(function() {
  var MessagesForm, OBJECT_TRIGGER, focus, triggered,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  OBJECT_TRIGGER = "#";

  triggered = false;

  focus = false;

  MessagesForm = (function(_super) {

    __extends(MessagesForm, _super);

    MessagesForm.prototype.events = {
      "click .message-type": "change_type",
      "click .save-btn": "save"
    };

    function MessagesForm() {
      MessagesForm.__super__.constructor.apply(this, arguments);
      this.start_autocomplete();
    }

    MessagesForm.prototype.save = function(e) {};

    MessagesForm.prototype.change_type = function(e) {
      var message_type, pointed, position;
      message_type = $(e.target);
      pointed = message_type.hasClass('type-pointed');
      if (!pointed) {
        $(".message-type").removeClass("type-pointed");
        $(".message-pointer").removeClass("pointed");
        message_type.addClass("type-pointed");
        position = message_type.attr('class').split(" ")[1];
        $(".type-pointers>." + position).addClass("pointed");
        if (message_type.attr('class').indexOf("info") !== -1) {
          if ($(".submenu").css("display") === 'block') {
            return $(".submenu").effect("drop", {}, 50);
          }
        } else {
          if ($(".submenu").css("display") !== 'block') {
            return $(".submenu").effect("slide", {}, 50);
          }
        }
      }
    };

    MessagesForm.prototype.start_autocomplete = function() {
      return $(".message").autocomplete({
        source: function(request, response) {
          var query_params;
          query_params = {
            'request': request.term
          };
          return transport_link.query('autocomplete', query_params, response);
        },
        search: function() {
          if (!triggered) {
            return false;
          }
        },
        select: function(event, ui) {
          var pos, text;
          text = this.value;
          pos = text.lastIndexOf(OBJECT_TRIGGER);
          this.value = text.substring(0, pos) + ' ' + OBJECT_TRIGGER + ui.item.value;
          triggered = false;
          focus = false;
          return false;
        },
        focus: function(event, ui) {
          focus = this.value;
          event.preventDefault();
          return true;
        }
      }).bind('keyup', function() {
        var index, last, len, query, text;
        if (!focus) {
          text = this.value;
          len = text.length;
          if (triggered) {
            index = text.lastIndexOf(OBJECT_TRIGGER);
            query = text.substring(index + OBJECT_TRIGGER.length);
            return $(this).autocomplete("search", query);
          } else {
            last = text.substring(len - OBJECT_TRIGGER.length);
            return triggered = last === OBJECT_TRIGGER;
          }
        }
      });
    };

    return MessagesForm;

  })(Spine.Controller);

  this.MessagesForm = MessagesForm;

}).call(this);
