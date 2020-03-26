import ajax from './ajax';
import { showToasts } from './toasts';

$(document).ready(() => {

    $('[data-event="delete-bookmark"]').on('click', async e => {
        e.preventDefault();
        const $bookmark = $(e.currentTarget);
        const data = await ajax({url: $bookmark.data('href'), method: 'DELETE'});
        showToasts(data);
        $(`[data-bookmark-guid="${$bookmark.data('bookmark-guid')}"]`).remove();
    });

    $('[data-event="scrape-bookmark"]').on('click', async e => {
        e.preventDefault();
        const $bookmark = $(e.currentTarget);
        const data = await ajax({url: $bookmark.data('href'), method: 'POST'});
        showToasts(data);
    });

});