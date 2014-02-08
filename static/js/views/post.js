var app = app || {};

app.PostView = Backbone.View.extend({
    tagName: 'div',
    className: 'post-list',
    template: _.template($('#postTemplate').html()),
    formErrorTemplate: _.template($('#formErrorTemplate').html()),

    events: {
        'click #comment-submit': 'submitComment',
        'click #delete-post': 'deletePost'
    },

    initialize: function() {
    },

    render: function() {
        this.$el.html( this.template( this.model.toJSON() ));
        return this;
    },

    validateField: function(field) {
        var value = field.val();
        if (value != '') {
            if (field[0].name != 'email' || (field[0].name == 'email' && this.validateEmail(value))) {
                return value;
            }else{
                field.after(this.formErrorTemplate({error_msg: 'Please enter a valid email address.'}));
                return false;
            }
        } else {
            field.after(this.formErrorTemplate({error_msg: 'This field is required'}));
            return false;
        }
    },

    validateEmail: function (email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    },

    parseCommentForm: function() {
        var author = {
            'name': this.validateField($('#comment-section input:eq(0)')),
            'email': this.validateField($('#comment-section input:eq(1)'))
        }
        var text = this.validateField($('#comment-section textarea'));
        if (author.name != false && author.email != false && text != false) {
            return JSON.stringify({ author: author, text: text });
        }else{
            return false;
        }
    },

    submitComment: function() {
        $('.alert').remove();
        data = this.parseCommentForm();
        if (data != false) {
            $.ajax({
                type: "POST",
                url: '/api/posts/' + this.model.id + '/comments',
                data: data,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                complete: this.onCommentAjaxComplete(this.model)
            });
        }
    },

    onCommentAjaxComplete: function(model) {
        return function(jqXHR, textStatus) {
            if (textStatus == 'error') {
                alert(jqXHR.responseText);
            } else {
                model.fetch();
            }
        }
    },

    deletePost: function() {
        // TODO: implement deletePost via ajax call to DELETE
    }

});