// Generated by CoffeeScript 1.3.3
(function() {
  var TemplateManager,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  TemplateManager = (function(_super) {

    __extends(TemplateManager, _super);

    function TemplateManager() {
      this.render = __bind(this.render, this);

      this.render_object = __bind(this.render_object, this);

      this.load_template = __bind(this.load_template, this);
      TemplateManager.__super__.constructor.apply(this, arguments);
      if (localStorage) {
        this.templates = localStorage;
      } else {
        this.templates = {};
      }
    }

    TemplateManager.prototype.load_template = function(template_name, callback) {
      var _this = this;
      return transport_link.query("templates", {
        'name': template_name
      }, function(data) {
        if (data != null ? data.template : void 0) {
          _this.templates[template_name] = data.template;
          return callback(data.template);
        }
      });
    };

    TemplateManager.prototype.render_object = function(object, callback) {
      var template;
      template = object.constructor.className.toLowerCase();
      template = "" + template + "/client/read.html";
      return this.render(template, object, callback);
    };

    TemplateManager.prototype.render = function(template, context, callback) {
      var _this = this;
      if (SETTINGS.debug || !this.templates[template]) {
        return this.load_template(template, function(template) {
          return callback(Mustache.render(template, context));
        });
      } else {
        template = this.templates[template];
        return callback(Mustache.render(template, context));
      }
    };

    return TemplateManager;

  })(Spine.Controller);

  this.templates = new TemplateManager();

}).call(this);
