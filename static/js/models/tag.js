/**
 * TagModel is a basic model to store tags used by the UniqueTagsCollection.
 */

var app = app || {};

app.TagModel = Backbone.Model.extend({
    defaults: {
        name: ''
    }
});