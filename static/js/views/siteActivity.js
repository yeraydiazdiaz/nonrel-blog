/**
 * ActivityView is a simple view to render a single activity.
 */
var app = app || {};

app.ActivityView = Backbone.View.extend({
    tagName: 'div',
    className: 'activity alert alert-dismissable',
    template: _.template($('#activityTemplate').html()),

    /**
     * Initialize an additional class depending on the type of task the
     * activity.
     */
    initialize: function() {
        var additional_class;
        if (this.model.get('task') == 'Deleted') {
            additional_class = 'alert-danger';
        } else if (this.model.get('task') == 'Created') {
            additional_class = 'alert-success';
        } else {
            additional_class = 'alert-info';
        }
        this.$el.addClass(additional_class);
    },

    /**
     * Basic rendering through template.
     * @returns {app.ActivityView} An instance of this view for render in parent view.
     */
    render: function() {
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    }
});

/**
 * SiteActivityView is associated with SiteActivities, rendering them as they are generated
 * and allowing the user to dismiss them.
 */
app.SiteActivitiesView = Backbone.View.extend({
    el: '#site-activity',

    /**
     * Set up handlers for changes on the SiteActivities collection.
     */
    initialize: function() {
        this.listenTo(app.blogCollection, 'sync', this.refreshView);
        this.listenTo(app.blogCollection, 'add', this.refreshView);
        this.listenTo(app.blogCollection, 'destroy', this.refreshView);
        this.listenTo(app.blogCollection, 'change', this.refreshView);
        this.listenTo(this.collection, 'sync', this.render);
    },

    /**
     * Render each activity sequentially, skipping the already rendered ones.
     * @returns {app.SiteActivitiesView} An instance of this view.
     */
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

    /**
     * Render a single activity, setting up the click handlers on the dismiss buttons.
     * When clicked we remove the model from the collection and update the timestamp
     * on the collection to not retrieve it again.
     * @param item The activity to be rendered.
     */
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

    /**
     * Handler for events on the collection. We do not remove models until the
     * user dismisses them.
     */
    refreshView: function() {
        this.collection.fetch({remove: false});
    }

});