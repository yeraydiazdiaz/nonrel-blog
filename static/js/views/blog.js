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
        this.listenTo(app.blogRouter, 'route:search', this.search);
        this.listenTo(app.blogRouter, 'route:tag', this.tag);
        this.listenTo(app.blogRouter, 'route:user', this.user);
        this.listenTo(app.blogRouter, 'route:viewPost', this.getModelFromCollectionOrFetch);
        this.listenTo(app.blogRouter, 'route:createPost', this.createPost);
        this.listenTo(app.blogRouter, 'route:editPost', this.editPost);
        // intercept search form submission
        $('.navbar-form').submit( function(view) {
            return function(e) {
                e.preventDefault();
                view.search(e.currentTarget[0].value);
                return false;
            }
        }(this));
    },

    // TODO: tags should be comma-separated, space-separated is dumb

    render: function(collection) {
        if (collection === undefined) {
            collection = this.collection;
        }
        if (this.postListView == undefined) {
            this.postListView = new app.PostListView({ collection: collection });
            this.$el.append(this.postListView.render().el);
        }
    },

    renderPostView: function(post) {
        this.postView = new app.PostView({
            model: post
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
        var post = this.collection.get(id);
        if (post == undefined) {
            post = new app.Post({id: id});
            this.collection.add(post);
            post.fetch({complete: this.onModelFetchComplete(this, 'Create', post), error: this.fetchError});
        }else{
            this.renderPostView(post);
        }
    },

    onModelFetchComplete: function(view, mode, post) {
        return function() {
            if (mode == 'Edit') {
                view.createEditPostView = new app.CreateEditPostView({model: post, mode: 'Edit'});
                view.$el.append(view.createEditPostView.render().el);
            }else{
                view.renderPostView(post);
            }
        }
    },

    fetchError: function() {
        alert('Fetch error');
    },

    home: function() {
        this.removeDetailViews();
        if (this.collection.url != '/api/posts') {
            this.collection.url = '/api/posts';
        }
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError, reset: true});
    },

    tag: function(param) {
        this.removeDetailViews();
        this.collection.url = '/api/posts/tag/' + param;
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
    },

    user: function(username) {
        this.removeDetailViews();
        this.collection.url = '/api/posts/user/' + username;
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
        if (this.postView) {
            var model = this.postView.model
            this.removeDetailViews();
            this.createEditPostView = new app.CreateEditPostView({model: model, mode: 'Edit'});
            this.$el.append(this.createEditPostView.render().el);
        }else{
            this.removeDetailViews();
            var post = new app.Post({id: id});
            this.collection.add(post);
            post.fetch({complete: this.onModelFetchComplete(this, 'Edit', post), error: this.fetchError});
        }
    },

    search: function(search_terms) {
        var terms = search_terms.trim();
        if (terms) {
            this.removeDetailViews();
            app.blogRouter.navigate('search/' + search_terms, {trigger: true});
            this.collection.url = '/api/posts/search/' + search_terms;
            this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
        }
    }

});