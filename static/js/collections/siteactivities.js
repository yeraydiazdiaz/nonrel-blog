
var app = app || {};

app.SiteActivitiesCollection = Backbone.Collection.extend({
    model: app.SiteActivityModel,
    url: '/api/siteactivities',
    comparator: 'timestamp'
});