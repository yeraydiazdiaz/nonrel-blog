
var app = app || {};

app.Post = Backbone.Model.extend({
    defaults: {
        id: null,
        title: '',
        text: '',
        tags: [],
        comments: [],
        user_name: '',
        user_id: null,
        created_on_readable: null
    }

});