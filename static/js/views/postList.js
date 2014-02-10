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

app.PostListView = Backbone.View.extend({
    tagName: 'div',

    events: {
        'click #load-more-posts': 'loadMorePosts'
    },

    initialize: function() {
        this.listenTo(this.collection, 'add', this.renderPostList);
        this.listenTo(this.collection, 'change', this.render);
        this.listenTo(this.collection, 'sync', this.render);
        this.listenTo(app.blogRouter, 'route:viewPost', this.hideView);
        this.listenTo(app.blogRouter, 'route:createPost', this.hideView);
        this.listenTo(app.blogRouter, 'route:home', this.showView);
        this.listenTo(app.blogRouter, 'route:user', this.showView);
        this.listenTo(app.blogRouter, 'route:tag', this.showView);
        this.listenTo(app.blogRouter, 'route:search', this.showView);
        this.hash = window.location.hash;
    },

    render: function() {
        if (this.collection.length > 0) {
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
        this.showView();
        return this;
    },

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

    renderPostList: function(item) {
        var postSnippetView = new app.PostSnippetView({
            model: item
        });
        this.$el.append(postSnippetView.render().el);
    },

    loadMorePosts: function() {
        $('#load-more-posts').remove();
        var lastDigit = this.collection.next.substring(
            this.collection.next.lastIndexOf('=')+1,
            this.collection.next.length
        )
        this.collection.fetch({remove: false, data: {page: Number(lastDigit)}});
    },

    hideView: function(param) {
        this.$el.hide();
    },

    showView: function(param) {
        if (this.hash == window.location.hash) {
            this.$el.fadeIn();
        }
        if (window.location.hash.indexOf('post') != 1) {
            this.hash = window.location.hash;
        }
    }

});