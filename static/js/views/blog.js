/**
 * BlogView is the base Backbone view for the app.
 * Creates the different views based on the routing and initial URL page.
 * Destroys views when they are no longer needed or need refreshing.
 */

var app = app || {};

app.BlogView = Backbone.View.extend({
    el: '#main',

    /**
     * initialize the view listening to resetting of the collection at bootstrap,
     * then all routing events to destroy and create views as needed.
     * Finally intercept the submission of the search view triggered either by clicking
     * on the button of the form or pressing Enter.
     */
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

    /**
     * Render the view using PostListView with different collections depending
     * on the page the user has navigated to.
     * @param collection Optionally pass a collection created on search, tag or author routes.
     */
    render: function(collection) {
        if (collection === undefined) {
            collection = this.collection;
        }
        if (this.postListView == undefined) {
            this.postListView = new app.PostListView({ collection: collection });
            this.$el.append(this.postListView.render().el);
        }
    },

    /**
     * Create a PostView with the passed Post instance
     * @param post The post instance to be rendered.
     */
    renderPostView: function(post) {
        this.postView = new app.PostView({
            model: post
        })
        this.$el.append(this.postView.render().el);
    },

    /**
     * Remove detail views (PostView or CreateEditView) if they exist.
     */
    removeDetailViews: function() {
        if (this.postView) {
            this.postView.remove();
        }
        if (this.createEditPostView) {
            this.createEditPostView.remove();
        }
    },

    /**
     * When routed to a post we first check to see if the model is already in the collection,
     * in the likely scenario that the user is browsing and clicked on a post. If not the user
     * has typed the URL manually which requires fetch from the server.
     * @param id ID of the post to be retrieved from the collection or the server.
     */
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

    /**
     * Handler of the successful fetch, returns an anonymous function to have the view
     * create the necessary view depending on the mode parameter.
     * @param view The Blog view instance to create the new views with.
     * @param mode A string representing the mode - create or edit
     * @param post The instance of the Post to be passed on to the new view.
     * @returns {Function}
     */
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

    /**
     * Handler of an error when fetching.
     */
    fetchError: function() {
        alert('Fetch error');
    },

    /**
     * Handles routes to the base URL deleting all detail views and fetching the collection.
     */
    home: function() {
        this.removeDetailViews();
        if (this.collection.url != '/api/posts') {
            this.collection.url = '/api/posts';
        }
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError, reset: true});
    },

    /**
     * Handles routes to the tag filtered view, deleting all detail views, changing the URL
     * on the collection and fetching.
     */
    tag: function(param) {
        this.removeDetailViews();
        this.collection.url = '/api/posts/tag/' + param;
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
    },

    /**
     * Handles routes to the user filtered view, deleting all detail views, changing the URL
     * on the collection and fetching.
     */
    user: function(username) {
        this.removeDetailViews();
        this.collection.url = '/api/posts/user/' + username;
        this.collection.fetch({success: this.onCollectionFetchComplete(this), error: this.fetchError});
    },

    /**
     * Handles the successful fetching of the collection on previous functions, rendering the
     * view passing the new collection.
     */
    onCollectionFetchComplete: function(view) {
        return function() {
            view.render(view.collection);
        }
    },

    /**
     * Handles routing to "Create new post", a special case CreateEdit view without a model to pass,
     * we do pass a base URL collection to ensure proper creation from the view.
     */
    createPost: function() {
        this.removeDetailViews();
        this.collection.url = '/api/posts';
        this.createEditPostView = new app.CreateEditPostView({collection: this.collection, mode: 'Create'})
        this.$el.append(this.createEditPostView.render().el);
    },

    /**
     * Handles routing to edit post, if the user was reading the post and we route we avoid fetching
     * the model and simply retrieve it from the PostView. Otherwise create a new Post instance and
     * fetch the data from the server.
     * @param id ID of the post to be retrieve from the server if needed.
     */
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

    /**
     * Handles routing to search, if the terms are valid set the appropriate URL for the API endpoint
     * and fetch.
     * @param search_terms Raw string passed from the search form.
     */
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