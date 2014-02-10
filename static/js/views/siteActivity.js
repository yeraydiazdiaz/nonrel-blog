var app = app || {};

app.ActivityView = Backbone.View.extend({
    tagName: 'div',
    className: 'activity alert alert-dismissable',
    template: _.template($('#activityTemplate').html()),

    initialize: function() {
        var additional_class;
        if (this.model.get('task') == 'Deleted') {
            additional_class = 'alert-danger';
        } else if (this.model.get('task') == 'Updated') {
            additional_class = 'alert-info';
        } else {
            additional_class = 'alert-success';
        }
        this.$el.addClass(additional_class);
    },

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
                if (!item.get('rendered')) {
                    this.renderActivities(item);
                    item.set({rendered: true});
                }
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
        view.$el.hide();
        this.$el.append(view.el);
        view.$el.fadeIn();
    },

    refreshView: function() {
        this.collection.fetch({remove: false});
    }

});