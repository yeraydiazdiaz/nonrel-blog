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
    }

});