
var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    initialize: function() {
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(app.blogRouter, 'route:viewPost', this.getFromCollectionOrFetch);
        this.listenTo(app.blogRouter, 'route:home', this.backToHome);
    },

    render: function() {
        this.postListView = new app.PostListView({ collection: this.collection });
        this.$el.append(this.postListView.render().el);
    },

    renderPostView: function() {
        this.postView = new app.PostView({
            model: this.post
        })
        this.$el.append(this.postView.render().el);
    },

    backToHome: function() {
        if (this.postView) {
            this.postView.remove();
        }
    },

    getFromCollectionOrFetch: function(id) {
        this.post = this.collection.get(id);
        if (this.post == undefined) {
            this.post = new app.Post({collection: this.collection, id: id});
            this.collection.add(this.post);
            this.post.fetch({complete: this.onModelFetchComplete, error: this.fetchError});
        }else{
            this.renderPostView();
        }
    },

    onModelFetchComplete: function() {
        app.blogView.renderPostView();
    },

    fetchError: function() {
        alert('Fetch error');
    }

});