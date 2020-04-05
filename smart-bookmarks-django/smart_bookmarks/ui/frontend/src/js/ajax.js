import Cookies from 'js-cookie';

const ajax = options => {
    const { url, method, data } = options;
    return $.ajax(url, {
        dataType: 'html',
        method: method,
        data: data,
        // processData: false,
        beforeSend: xhr => {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    })
};

const setupAjax = () => {
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  const csrftoken = Cookies.get('csrftoken');

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });
};

$(document).ready(() => {
   setupAjax();
});

export default ajax;
