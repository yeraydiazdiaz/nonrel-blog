/**
 * Post model for the blog. Mimics the Django model with default values.
 */

var app = app || {};

app.Post = Backbone.Model.extend({
    defaults: {
        id: null,
        title: '',
        permalink: '',
        text: '',
        tags: [],
        comments: [],
        user_name: '',
        user_id: null,
        created_on_readable: null,
        updated_on_readable: null
    },

    urlRoot: function() {
        if (this.get('id') == null && this.get('permalink')) {
            return this.collection.url + '/' + this.get('permalink');
        } else {
            return this.collection.url
        }
    }

});