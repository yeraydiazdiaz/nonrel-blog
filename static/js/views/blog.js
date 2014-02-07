
var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    initialize: function() {
        this.listenTo(app.blogRouter, 'route:home', this.home);
        this.listenTo(app.blogRouter, 'route:tag', this.tag);
        this.listenTo(app.blogRouter, 'route:viewPost', this.getModelFromCollectionOrFetch);
        this.listenTo(app.blogRouter, 'route:createPost', this.createPost);
    },

    render: function(collection) {
        if (collection === undefined) {
            collection = this.collection;
        }
        this.postListView = new app.PostListView({ collection: collection });
        this.$el.append(this.postListView.render().el);
    },

    renderPostView: function() {
        this.postView = new app.PostView({
            model: this.post
        })
        this.$el.append(this.postView.render().el);
    },

    removeDetailViews: function() {
        if (this.postView) {
            this.postView.remove();
        }
        if (this.createPostView) {
            this.createPostView.remove();
        }
    },

    getModelFromCollectionOrFetch: function(id) {
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
    },

    home: function() {
        this.removeDetailViews();
        if (this.collection.url != '/api/posts') {
            this.postListView.remove();
            this.collection.url = '/api/posts';
            this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
        } else if (this.collection.models.length <= 1 && this.postListView == undefined) {
            this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
        }
    },

    tag: function(param) {
        this.removeDetailViews();
        this.postListView.remove();
        this.collection.url = '/api/posts/tag/' + param;
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
    },

    onCollectionFetchComplete: function(view) {
        return function() {
            view.render(view.collection);
        }
    },

    createPost: function() {
        this.removeDetailViews();
        this.createPostView = new app.CreatePostView();
        this.$el.append(this.createPostView.render().el);
    }

});