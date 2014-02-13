/**
 * Post model for the blog. Mimics the Django model with default values.
 */

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
        created_on_readable: null,
        updated_on_readable: null
    }

});