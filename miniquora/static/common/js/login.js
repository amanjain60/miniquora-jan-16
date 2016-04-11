login = (function() {
  function handlelogin(e) {
    e.preventDefault();
    data = new FormData($('form')[0]);
    $.ajax({
      url: '/account/login/',
      type:"POST",
      data: data,
      processData: false,
      dataType: 'json',
      contentType: false,
      success: function(response, xhr) {
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
  function init() {
    $('#login-btn').click(handlelogin);
  }
  return {
    init : init
  };
})();
