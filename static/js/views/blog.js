/**
 * BlogView is the base Backbone view for the app. It holds the main collection and
 * shifts in and out the rest of the views as needed.
 */

var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    initialize: function() {
        this.listenToOnce(this.collection, 'reset', this.render);
        this.listenTo(app.blogRouter, 'route:home', this.home);
        this.listenTo(app.blogRouter, 'route:tag', this.tag);
        this.listenTo(app.blogRouter, 'route:viewPost', this.getModelFromCollectionOrFetch);
        this.listenTo(app.blogRouter, 'route:createPost', this.createPost);
        this.listenTo(app.blogRouter, 'route:editPost', this.editPost);
    },

    // TODO: tags should be comma-separated, space-separated is dumb

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
        if (this.createEditPostView) {
            this.createEditPostView.remove();
        }
    },

    getModelFromCollectionOrFetch: function(id) {
        this.removeDetailViews();
        this.post = this.collection.get(id);
        if (this.post == undefined) {
            this.post = new app.Post({collection: this.collection, id: id});
            this.collection.add(this.post);
            this.post.fetch({complete: this.onModelFetchComplete(this, 'Create'), error: this.fetchError});
        }else{
            this.renderPostView();
        }
    },

    onModelFetchComplete: function(view, mode) {
        return function() {
            if (mode == 'Edit') {
                view.createEditPostView = new app.CreateEditPostView({collection: view.collection, model: view.post, mode: 'Edit'});
                view.$el.append(view.createEditPostView.render().el);
            }else{
                view.renderPostView();
            }
        }
    },

    fetchError: function() {
        alert('Fetch error');
    },

    home: function() {
        this.removeDetailViews();
        // we refetch the collection if we're coming back from a tag view.
        if (this.collection.url != '/api/posts') {
            this.postListView.remove();
            this.collection.url = '/api/posts';
            this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError, reset: true});
        }
    },

    tag: function(param) {
        this.removeDetailViews();
        if (this.postListView) {
            this.postListView.remove();
        }
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
        this.createEditPostView = new app.CreateEditPostView({collection: this.collection, mode: 'Create'})
        this.$el.append(this.createEditPostView.render().el);
    },

    editPost: function(id) {
        this.removeDetailViews();
        if (this.postView) {
            this.post = this.postView.model;
            this.createEditPostView = new app.CreateEditPostView({collection: this.collection, model: this.post, mode: 'Edit'});
            this.$el.append(this.createEditPostView.render().el);
        }else{
            this.post = new app.Post({collection: this.collection, id: id});
            this.collection.add(this.post);
            this.post.fetch({complete: this.onModelFetchComplete(this, 'Edit'), error: this.fetchError});
        }
    }

});