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
        this.listenTo(app.blogCollection, 'sync', this.refreshView);
        this.listenTo(this.collection, 'sync', this.render);
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
        var view = activityView.render();
        view.$el.find('button').click( function(collection, model) {
            return function() {
                collection.remove(model);
                collection.updateTimestamp();
            }
        }(this.collection, item));
        this.$el.append(view.el);
    },

    refreshView: function() {
        this.$el.html('');
        this.collection.fetch({remove: false});
    }

});