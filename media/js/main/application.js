// Generated by CoffeeScript 1.3.3
(function() {
  var Application,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __slice = [].slice;

  Application = (function(_super) {

    __extends(Application, _super);

    Application.currentview;

    function Application(config) {
      this.show_controller = __bind(this.show_controller, this);

      this.next_url = __bind(this.next_url, this);

      var _this = this;
      Application.__super__.constructor.apply(this, arguments);
      this.views = {
        'auth': new Auth({
          'el': $(".auth_form"),
          'user': config.user
        }),
        'messages': new Messages({
          'el': $(".content")
        })
      };
      this.views['auth'].bind("authentification_required", function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return _this.navigate("/login/");
      });
      this.routes({
        "/messages/": function() {
          return _this.show_controller('messages');
        },
        "/login/": function() {
          return _this.show_controller('auth', {
            'redirect': location.hash
          });
        }
      });
      if (this.views['auth'].is_authentificated()) {
        this.navigate("/messages/");
      } else {
        this.navigate("/login/");
      }
      Spine.Route.setup();
    }

    Application.prototype.next_url = function() {
      return "/messages/";
    };

    Application.prototype.show_controller = function() {
      var args, currentview_name, options, screen, show_effect, view, view_name, _ref, _ref1,
        _this = this;
      screen = arguments[0], options = arguments[1], args = 3 <= arguments.length ? __slice.call(arguments, 2) : [];
      if (screen == null) {
        screen = 'messages';
      }
      if (options == null) {
        options = {};
      }
      if (typeof screen === 'string') {
        screen = this.views[screen];
      }
      $(".open").removeClass("open");
      if (this.currentview !== screen) {
        show_effect = false;
        if (this.currentview) {
          this.currentview.unbind('exit');
          this.currentview.el.effect('slide', {
            'direction': 'right',
            'mode': 'hide'
          });
          this.currentview.el.hide();
          show_effect = true;
        }
        this.currentview = screen;
        _ref = this.views;
        for (view_name in _ref) {
          view = _ref[view_name];
          if (view === this.currentview) {
            currentview_name = view_name;
          }
        }
        document.title = screen.title;
        if (show_effect) {
          screen.el.show();
        } else {
          screen.el.show();
        }
        screen.trigger("enter");
        _ref1 = this.views;
        for (view_name in _ref1) {
          view = _ref1[view_name];
          if (view !== this.currentview) {
            view.trigger("new_view", currentview_name);
          }
        }
        if (options.redirect) {
          return screen.bind("exit", function(args) {
            return _this.navigate(options.redirect);
          });
        } else {
          return screen.bind("exit", function() {
            var action, args;
            action = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
            if (action != null ? action.indexOf("/" === 0) : void 0) {
              return _this.navigate(action);
            } else if (action) {
              return _this.show_controller(action);
            } else {
              return _this.navigate("/messages/");
            }
          });
        }
      }
    };

    return Application;

  })(Spine.Controller);

  this.Application = Application;

}).call(this);
