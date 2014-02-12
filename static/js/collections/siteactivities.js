/**
 * The SiteActivitiesCollection holds the all activities retrieved from the server.
 * The back-end is set up to allow an optional timestamp at the end to retrieve only
 * activities that have a higher timestamp. On startup a current timestamp is generated.
 * @type {app|*|app|*|{}|app|*|app|*|{}|{}|{}}
 */

var app = app || {};

app.SiteActivitiesCollection = Backbone.Collection.extend({
    model: app.SiteActivityModel,
    base_url: '/api/siteactivities',
    url: '/api/siteactivities',
    comparator: 'timestamp',

    initialize: function() {
        this.updateTimestamp();
    },

    /**
     * Updates the URL adding the current timestamp to retrieve activities
     * created from this point on.
     */
    updateTimestamp: function() {
        var timestamp = new Date().getTime()/1000;
        timestamp = Math.round(timestamp);
        this.url = this.base_url + '/' + timestamp;
    }

});