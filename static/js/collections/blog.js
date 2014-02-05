
var app = app || {};

app.Blog = Backbone.Collection.extend({
    model: app.Post,
    url: '/api/posts',

    parse: function(data) {
        this.count = data.count;
        this.next = data.next;
        this.previous = data.previous;
        return data.results;
    }
});