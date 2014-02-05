var app = app || {};

app.PostView = Backbone.View.extend({
    tagName: 'div',
    className: 'post-list',
    template: _.template($('#postTemplate').html()),

    render: function() {
        // this.el is what we defined in tagName, use $el to access the jQuery html() function.
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    }
});