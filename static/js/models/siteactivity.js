/**
 * The SiteActivityModel for the SiteActivityCollection. Mimics the Django model.
 */

var app = app || {};

app.SiteActivityModel = Backbone.Model.extend({
    defaults: {
        post_title: '',
        post_id: null,
        user_name: '',
        user_id: null,
        created_on_readable: null,
        timestamp: null,
        task: '',
        rendered: false

    }

});