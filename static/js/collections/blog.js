/**
 * The BlogCollection will hold Post instances.
 * The back-end API uses paginated results hence the special parsing.
 * @type {app|*|{}}
 */


var app = app || {};

app.BlogCollection = Backbone.Collection.extend({
    model: app.Post,
    url: '/api/posts',
    // SortBy comparator function matching the ordering from the back-end.
    comparator: function(a, b) {
        if (a.get('timestamp') > b.get('timestamp')) {
            return -1;
        } else if (a.get('timestamp') < b.get('timestamp')) {
            return 1;
        } else {
            return 0;
        }
    },

    /**
     * Parse the data from the API, in some instances, like when adding a post, the
     * API will not return paginated results. In that case keep the previous values.
     * @param data Data returned by the back-end API.
     * @returns {*} Data to be processed by the Collection.
     */
    parse: function(data) {
        if (data.count != null) {
            this.count = data.count;
            this.next = data.next;
            this.previous = data.previous;
            return data.results;
        } else {
            return data;
        }
    }
});