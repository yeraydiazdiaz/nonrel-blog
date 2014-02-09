var app = app || {};

app.ActivityView = Backbone.View.extend({
    template: _.template($('#activityTemplate').html()),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    }
});

app.SiteActivitiesView = Backbone.View.extend({
    el: '#site-activity',

    initialize: function() {
        this.listenTo(this.collection, 'add', this.renderActivities);
        this.listenTo(this.collection, 'destroy', this.refreshView);
        this.listenTo(app.blogCollection, 'sync', this.refreshView);
    },

    render: function() {
        if (this.collection.length > 0) {
            this.collection.each(function(item) {
                this.renderActivities(item);
            }, this);
        }
        return this;
    },

    renderActivities: function(item) {
        var activityView = new app.ActivityView({
            model: item
        });
        var temp = activityView.render().el;
        this.$el.append(temp);
    },

    refreshView: function() {
        this.$el.html('');
        this.collection.fetch();
        this.render();
    }

});