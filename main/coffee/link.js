// Generated by CoffeeScript 1.3.3
var Link, QueueManager,
  __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

QueueManager = (function() {

  function QueueManager() {
    this.cache = {};
  }

  QueueManager.prototype.register = function(callback, tags, limit) {
    var tag, _i, _len, _ref, _results;
    tags = tags;
    limit = limit || 1;
    _ref = tags.split(",");
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      tag = _ref[_i];
      if (__indexOf.call(this.cache, tag) < 0) {
        this.cache[tag] = [];
      }
      _results.push(this.cache[tag].push({
        "fnc": callback,
        "limit": limit
      }));
    }
    return _results;
  };

  QueueManager.prototype.callback = function(name, data) {
    var callback, callbacks, _i, _len, _results;
    callbacks = this.cache[name];
    if (callbacks) {
      _results = [];
      for (_i = 0, _len = callbacks.length; _i < _len; _i++) {
        callback = callbacks[_i];
        callback['fnc'](data);
        if (callback['limit']) {
          callback['limit'] -= 1;
          if (callback['limit'] === 0) {
            _results.push(delete this.cache[name]);
          } else {
            _results.push(void 0);
          }
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    }
  };

  return QueueManager;

})();

Link = (function() {

  Link.connected = false;

  Link.transport = false;

  Link.reconnect = true;

  Link.queues = false;

  function Link(config) {
    this.config = config;
    config = SETTINGS.transport;
    this.connect(config.address, config.port);
    this.queues = new QueueManager();
    this.reconnect = false;
  }

  Link.prototype.connect = function(address, port) {
    this.transport = new SockJS("http://" + address + ":" + port + "/transport/");
    this.transport.onopen = function() {
      return window.link.connected();
    };
    this.transport.onclose = function() {
      return window.link.disconnected();
    };
    return this.transport.onmessage = function(e) {
      return window.link.process_message(e);
    };
  };

  Link.prototype.connected = function() {
    return this.connected = true;
  };

  Link.prototype.disconnected = function() {
    this.connected = false;
    if (this.reconnect) {
      return this.connect();
    }
  };

  Link.prototype.process_message = function(e) {
    var data, tag, tag_data, _results;
    data = $.parseJSON(e.data);
    _results = [];
    for (tag in data) {
      tag_data = data[tag];
      _results.push(this.queues.callback(tag, tag_data));
    }
    return _results;
  };

  Link.prototype.query = function(tag, params, callback) {
    var data, is_blocking, message;
    is_blocking = is_blocking || false;
    if (typeof callback === 'function') {
      this.queues.register(callback, tag);
    }
    data = {
      'params': params,
      'tags': [tag]
    };
    message = JSON.stringify(data);
    return this.transport.send(message);
  };

  Link.prototype.subscribe = function(tags, callback) {
    return this.queues.register(callback, tag);
  };

  return Link;

})();

$(document).ready(function() {
  return window.link = new Link({});
});
