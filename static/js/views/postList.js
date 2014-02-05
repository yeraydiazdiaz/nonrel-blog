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
        this.listenTo(this.collection, 'sync', this.checkForMorePosts);
    },

    render: function() {
        this.collection.each(function(item) {
            this.renderPostList(item);
        }, this);
        return this;
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
        this.collection.fetch({data: {page: Number(lastDigit)}});
    },

    checkForMorePosts: function() {
        if (this.collection.next !== null) {
            this.$el.append($('#loadMoreTemplate').html());
        }
    }

});