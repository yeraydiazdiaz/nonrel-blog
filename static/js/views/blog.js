
var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    initialize: function() {
        this.collection = new app.Blog();
        this.collection.fetch({reset: true});

        this.listenTo(this.collection, 'reset', this.render);
    },

    render: function() {
        var postListView = new app.PostListView({
            collection: this.collection
        });
        this.$el.append(postListView.render().el);
    }

});