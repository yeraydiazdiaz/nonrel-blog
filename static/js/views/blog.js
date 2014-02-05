
var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    initialize: function() {
        this.collection = new app.Blog();
        this.collection.fetch({reset: true});

        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(app.BlogRouter, 'route:viewPost', this.renderPostView);
        this.listenTo(app.BlogRouter, 'route:home', this.backToHome);
    },

    render: function() {
        this.postListView = new app.PostListView({
            collection: this.collection
        });
        this.$el.append(this.postListView.render().el);
    },

    renderPostView: function(param) {
        this.postView = new app.PostView({
            model: this.collection.get(param)
        })
        this.$el.append(this.postView.render().el);
    },

    backToHome: function() {
        this.postView.remove();
    }

});