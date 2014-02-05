
var app = app || {};

app.Post = Backbone.Model.extend({
    defaults: {
        title: 'No title',
        text: 'No text',
        author: 'Unknown',
        created_on: 'Unknown',
        tags: [],
        comments: []
    }
});