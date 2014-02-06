var app = app || {};

app.PostView = Backbone.View.extend({
    tagName: 'div',
    className: 'post-list',
    template: _.template($('#postTemplate').html()),

    events: {
        'click #comment-submit': 'submitComment'
    },

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    },

    submitComment: function() {
        var author = {
            'name': $('#comment-section input').get(0).value,
            'email': $('#comment-section input').get(1).value
        }
        var text = $('#comment-section input').get(2).value
        alert(JSON.stringify({ author: author, text: text}))
        $.ajax({
            type: "POST",
            url: '/api/posts/' + this.model.id + '/comments',
            data: JSON.stringify({ author: author, text: text}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){alert(data);},
            failure: function(errMsg) {
                alert(errMsg);
            },
            complete: this.onComplete
        });
    },

    onComplete: function(jqXHR, textStatus) {
        alert(textStatus);
    }

});