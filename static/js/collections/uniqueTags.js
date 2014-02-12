/**
 * UniqueTagsCollection is a basic Collection to store the current list
 * of unique tags retrieved from the server.
 */

var app = app || {};

app.UniqueTagsCollection = Backbone.Collection.extend({
    model: app.TagModel,
    url: '/api/alltags',
    comparator: 'name',

    /**
     * The back-end will return an array of tags, models require objects so
     * we create one with {name: tag}.
     * @param data Array of tags from the back-end.
     * @returns {Array|*} Array of objects in the form {name: tag}.
     */
    parse: function(data) {
        parsed_data = new Array();
        for (d in data) {
            parsed_data.push({name: data[d]});
        }
        return parsed_data;
    }
});