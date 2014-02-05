
var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    events: {
    },

    initialize: function() {
        this.blogCollection = new app.Blog();
        this.blogCollection.fetch({reset: true});

        this.listenTo(this.blogCollection, 'reset', this.render);
    },

    render: function() {
        var postListView = new app.PostListView({
            collection: this.blogCollection
        });
        this.$el.append(postListView.render().el);
    }

});