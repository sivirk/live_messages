// Generated by CoffeeScript 1.3.3
(function() {
  var Messages,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __slice = [].slice;

  Messages = (function(_super) {

    __extends(Messages, _super);

    Messages.extend(Spine.Events);

    function Messages() {
      this.on_show = __bind(this.on_show, this);

      this.on_update = __bind(this.on_update, this);

      this.update = __bind(this.update, this);

      this.insert = __bind(this.insert, this);

      var _this = this;
      Messages.__super__.constructor.apply(this, arguments);
      this.title = 'Журналы';
      this.form = new MessagesForm({
        el: ".message-form"
      });
      this.bind("enter", this.on_show);
      this.bind("update", this.on_update);
      Message.bind("created", function(message) {
        return _this.insert(message);
      });
    }

    Messages.prototype.insert = function(message, index) {
      var _this = this;
      if (index == null) {
        index = 0;
      }
      return templates.render_object(message, function(html) {
        return console.log(html);
      });
    };

    Messages.prototype.update = function(params) {
      var dairy_list;
      dairy_list = $(".dairy-list");
      $("li", dairy_list).removeClass('active');
      $(".dairy__" + params.dairy).addClass('active');
      if ($(".dairy__" + params.dairy).length) {
        return 'asda';
      }
    };

    Messages.prototype.on_update = function() {
      var args, params;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      if (args != null ? args.length : void 0) {
        params = args[0];
        return this.update(params);
      }
    };

    Messages.prototype.on_show = function() {
      var args, dairy_list, params,
        _this = this;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      if (args != null ? args.length : void 0) {
        params = args[0];
        this.update(params);
      }
      dairy_list = $(".dairy-list");
      if (!$("li", dairy_list).length) {
        return transport_link.query('dairy', {}, function(result) {
          var active, dairy, dairy_name, dairy_url, url, _i, _len;
          url = null;
          active = '';
          for (_i = 0, _len = result.length; _i < _len; _i++) {
            dairy = result[_i];
            dairy_name = dairy.slug;
            dairy_url = "/messages/" + dairy_name + "/";
            if (!url) {
              url = dairy_url;
            }
            dairy = $(("<li class='dairy__" + dairy_name + " " + active + "'><a href='#" + dairy_url + "'>") + dairy.title + "</a></li>");
            dairy_list.append(dairy);
          }
          return _this.navigate(url);
        });
      }
    };

    return Messages;

  })(Spine.Controller);

  this.Messages = Messages;

}).call(this);
