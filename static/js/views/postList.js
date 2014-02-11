/**
 * PostListView and PostSnippetView
 * PostSnippetView is a simple view to represent a Post without too much data.
 * PostListView is rendered as a sequence of PostSnippetViews.
 */

var app = app || {};

app.PostSnippetView = Backbone.View.extend({
    tagName: 'div',
    className: 'post-list',
    template: _.template($('#postListTemplate').html()),

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    }
});

/**
 * PostListView is kept in memory as it is the central hub for the blog.
 * The BlogView feeds different collections to which PostListView listens
 * for events and reacts.
 */
app.PostListView = Backbone.View.extend({
    tagName: 'div',
    loadingIconTag: '<img src="/static/img/loaderb64.gif" id="loading-icon" />',

    events: {
        'click #load-more-posts': 'loadMorePosts'
    },

    /**
     * Initialize the view by listening to the current collection event and routes.
     */
    initialize: function() {
        this.dirty = true;
        this.pendingFade = false;
        this.$el.hide();
        this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(this.collection, 'add', this.setToDirty);
        this.listenTo(this.collection, 'destroy', this.setToDirty);
        this.listenTo(app.blogRouter, 'route:viewPost', this.hideView);
        this.listenTo(app.blogRouter, 'route:createPost', this.hideView);
        this.listenTo(app.blogRouter, 'route:editPost', this.hideView);
        this.listenTo(app.blogRouter, 'route:home', this.showView);
        this.listenTo(app.blogRouter, 'route:user', this.showView);
        this.listenTo(app.blogRouter, 'route:tag', this.showView);
        this.listenTo(app.blogRouter, 'route:search', this.showView);
    },

    /**
     * Rendering consists on a message and the render of each snippet.
     * @returns {app.PostListView}
     */
    render: function(e) {
        if (this.dirty) {
            if (this.collection.length > 0) {
                this.collection.sort();
                this.$el.html('<h1>' + this.getHeadingMessage() +'</h1>');
                this.collection.each(function(item) {
                    this.renderPostList(item);
                }, this);
                if (this.collection.next != null
                    && this.collection.next != 'None'
                    && $('#load-more-posts').get(0) == undefined) {
                    this.$el.append($('#loadMoreTemplate').html());
                }
            } else {
                this.$el.html('<h1>No results</h1>');
            }
            this.dirty = false;
            if (this.pendingFade) {
                this.showView();
            }
        }
        return this;
    },

    /**
     * Details of the rendering of the item, creates the PostSnippetView and renders it.
     * @param item Instance of the model to be rendered.
     */
    renderPostList: function(item) {
        var postSnippetView = new app.PostSnippetView({
            model: item
        });
        this.$el.append(postSnippetView.render().el);
    },

    /**
     * Returns a message with information about the nature of the content being displayed
     * @returns {string} Contextual message defining the nature of the content.
     */
    getHeadingMessage: function() {
        if (this.collection.url.indexOf('search') != -1) {
            return 'Search results for: ' + this.collection.url.substr(this.collection.url.lastIndexOf('/')+1)
        } else if (this.collection.url.indexOf('tag') != -1) {
            return 'Posts with tag: ' + this.collection.url.substr(this.collection.url.lastIndexOf('/')+1)
        } else if (this.collection.url.indexOf('user') != -1) {
            return 'Posts by user: ' + this.collection.url.substr(this.collection.url.lastIndexOf('/')+1)
        } else {
            return '';
        }

    },

    /**
     * Implements the fetching of more posts on demand. Uses pagination on the server side
     * to request the next set.
     */
    loadMorePosts: function() {
        $('#load-more-posts').remove();
        var lastDigit = this.collection.next.substring(
            this.collection.next.lastIndexOf('=')+1,
            this.collection.next.length
        )
        this.collection.fetch({remove: false, data: {page: Number(lastDigit)}});
    },

    /**
     * Hides the view reacting to a route event.
     * @param param Parameter from the route event.
     */
    hideView: function() {
        this.$el.hide();
    },

    /**
     * Fades in the view taking into account if the collection has changed
     * and the view hasn't been re-rendered yet.
     * @param param Parameter from the route event.
     */
    showView: function() {
        if (!this.dirty) {
            this.$el.fadeIn();
            this.pendingFade = false;
        }else{
            this.$el.html(this.loadingIconTag);
            this.pendingFade = true;
        }
    },

    /**
     * Removes content of view and prepares for syncing from collection and render.
     */
    setToDirty: function() {
        this.dirty = true;
        this.$el.html(this.loadingIconTag);
    }

});