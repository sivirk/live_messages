// Generated by CoffeeScript 1.3.3
var Auth,
  __slice = [].slice;

Auth = (function() {

  function Auth() {
    window.link.subscribe('auth.error', this.exception);
  }

  Auth.prototype.exception = function() {
    var args;
    args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
  };

  return Auth;

})();

$(document).ready(function() {
  return window.auth = new Auth();
});