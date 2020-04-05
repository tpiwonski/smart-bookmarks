import ajax from './ajax';
import { showToasts } from './toasts';

$(document).ready(() => {

    $('[data-event="delete-bookmark"]').on('click', async e => {
        e.preventDefault();
        const $bookmark = $(e.currentTarget);
        const data = await ajax({url: $bookmark.data('href'), method: 'DELETE'});
        // showToasts(data);
        // $(`[data-bookmark-guid="${$bookmark.data('bookmark-guid')}"]`).remove();
        window.location = window.location;
    });

    $('[data-event="scrape-bookmark"]').on('click', async e => {
        e.preventDefault();
        const $bookmark = $(e.currentTarget);
        // const data = await ajax({url: $bookmark.data('href'), method: 'POST', data: {lorem: "ipsum"}});
        const data = await $.post($bookmark.data('href'), {"redirect": window.location.href});
        // showToasts(data);
        window.location = window.location;
    });

});
