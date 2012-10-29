// Generated by CoffeeScript 1.3.3
(function() {
  var Auth,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Auth = (function(_super) {

    __extends(Auth, _super);

    Auth.extend(Spine.Events);

    function Auth(config) {
      this.logout = __bind(this.logout, this);

      this.login = __bind(this.login, this);

      this.updateUserInfo = __bind(this.updateUserInfo, this);

      this.on_show = __bind(this.on_show, this);

      this.is_authentificated = __bind(this.is_authentificated, this);
      Auth.__super__.constructor.apply(this, arguments);
      this.title = 'Авторизация';
      this.user = config.user;
      this.bind("enter", this.on_show);
      this.bind("new_view", this.updateUserInfo);
      $(".auth-btn").on('click', this.login);
      $(".auth-logout").on('click', this.logout);
      transport_link.subscribe('auth.error', this.go_authentificate);
    }

    Auth.prototype.is_authentificated = function() {
      var _ref;
      if ((_ref = this.user) != null ? _ref.user_id : void 0) {
        return true;
      } else {
        return false;
      }
    };

    Auth.prototype.on_show = function() {
      if (this.user_id) {
        return this.navigate(application.next_url());
      }
    };

    Auth.prototype.updateUserInfo = function(view) {
      var user_info;
      if (view === 'messages') {
        user_info = $(".user-info > span");
      }
      if (this.user.user_name) {
        return user_info.html(this.user.user_name);
      }
    };

    Auth.prototype.go_authentificate = function(exception) {};

    Auth.prototype.login = function(e) {
      var _this = this;
      transport_link.send_form(".login-form form", function(result) {
        if (result.success) {
          _this.user = result.user;
          return _this.trigger("exit");
        } else {

        }
      });
      return false;
    };

    Auth.prototype.logout = function(e) {
      var _this = this;
      transport_link.query("logout", {}, function(result) {
        if (result.success) {
          _this.user = null;
          return _this.trigger('authentification_required');
        }
      });
      return false;
    };

    return Auth;

  })(Spine.Controller);

  this.Auth = Auth;

}).call(this);
