import Cookies from 'js-cookie';

const ajax = options => {
    const { url, method } = options;
    return $.ajax(url, {
        dataType: 'html',
        method: method,
        beforeSend: xhr => {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
    })
};

export default ajax;
