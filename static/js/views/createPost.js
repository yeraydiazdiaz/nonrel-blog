var app = app || {};

app.CreatePostView = Backbone.View.extend({
    template: _.template($('#postFormTemplate').html()),
    formErrorTemplate: _.template($('#formErrorTemplate').html()),
    postTemplate: _.template($('#postTemplate').html()),

    events: {
        'click #preview-post': 'previewPost',
        'click #submit-post': 'submitPost'
    },

    render: function() {
        this.$el.html( this.template() )
        return this;
    },

    validateField: function(field) {
        var value = field.val();
        if (value != '') {
            return value;
        } else {
            field.after(this.formErrorTemplate({error_msg: 'This field is required'}));
            return false;
        }
    },

    parsePostForm: function() {
        var title = this.validateField($('#post-title'));
        var text = this.validateField($('#post-text'));
        var tags = $('#post-tags').val();
        if (tags == '') {
            tags = null;
        }
        if (title != false && text != false) {
            return JSON.stringify({ title: title, text: text, tags: tags });
        }else{
            return false;
        }
    },

    previewPost: function() {
        $('.alert').remove();
        data = this.parsePostForm();
        if (data != false) {
            data = JSON.parse(data);
            if (data.tags != null) {
                data.tags = data.tags.split(' ');
            }
            data.created_on_readable = '<strong>Just now</strong>';
            data.comments = [];
            data.skipCommentsForm = true;
            this.$('#post-preview').html( this.postTemplate(data) );
        }
    },

    submitPost: function() {
        $('.alert').remove();
        data = this.parsePostForm();
        if (data != false) {
            var csrftoken = this.getCookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            });
            $.ajax({
                type: 'POST',
                url: '/api/posts',
                data: data,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                complete: this.onCommentAjaxComplete(this.model),
                xhrFields: {
                  withCredentials: true
                }
            });
        }
    },

    onCommentAjaxComplete: function(model) {
        return function(jqXHR, textStatus) {
            if (textStatus == 'error') {
                alert(jqXHR.responseText);
            } else {
                var response = JSON.parse(jqXHR.responseText);
                app.blogRouter.navigate('', {trigger: true} );
            }
        }
    },

    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});