import 'bootstrap';

export const showToasts = data => {
    $('#toasts').replaceWith($(data).find('#toasts'));
    $('.toast').toast('show');
};

$(document).ready(() => {
    $('.toast').toast('show');
});
