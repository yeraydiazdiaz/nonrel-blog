
var app = app || {};

app.SiteActivitiesCollection = Backbone.Collection.extend({
    model: app.SiteActivityModel,
    base_url: '/api/siteactivities',
    url: '/api/siteactivities',
    comparator: 'timestamp',

    initialize: function() {
        this.updateTimestamp();
    },

    updateTimestamp: function() {
        var timestamp = new Date().getTime()/1000;
        timestamp = Math.round(timestamp);
        this.url = this.base_url + '/' + timestamp;
    }

});