var app = app || {};

app.CreateEditPostView = Backbone.View.extend({
    template: _.template($('#postFormTemplate').html()),
    formErrorTemplate: _.template($('#formErrorTemplate').html()),
    postTemplate: _.template($('#postTemplate').html()),

    events: {
        'click #preview-post': 'previewPost',
        'click #submit-post': 'submitPost'
    },

    initialize: function(options) {
        this.mode = options.mode;
    },

    render: function() {
        if (this.model) {
            var json = this.model.toJSON();
            json.mode = this.mode;
            this.$el.html( this.template(json) )
        }else{
            this.$el.html( this.template( {title: '', text: '', tags: [], mode: this.mode}) )
        }
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
        var tags = $('#post-tags').val().trim();
        if (tags == '') {
            tags = [];
        }else{
            tags = tags.split(' ');
        }
        if (title != false && text != false) {
            return { title: title, text: text, tags: tags };
        }else{
            return false;
        }
    },

    previewPost: function() {
        this.$el.find('.alert').remove();
        var data = this.parsePostForm();
        if (data != false) {
            // forms and admin buttons are not shown in previews
            data.skipEditButtons = true;
            data.skipCommentsForm = true;
            if (this.model) {
                // we're previewing the edition of a post, pass as much data from it as possible
                var jsonModel = this.model.toJSON();
                data.created_on_readable = jsonModel.created_on_readable;
                if (!data.hasOwnProperty('tags')) {
                    data.tags = jsonModel.tags;
                }
                data.comments = jsonModel.comments;
                data.user_id = jsonModel.user_id;
                data.user_name = jsonModel.user_name;
                data.id = jsonModel.id;
            }else{
                data.user_name = $('.dropdown-toggle').html().substring(0, $('.dropdown-toggle').html().indexOf('<')-1);
                data.created_on_readable = 'just now';
                data.comments = [];
            }
            this.$('#post-preview').html( this.postTemplate(data) );
        }
    },

    submitPost: function() {
        this.$el.find('.alert').remove();
        var data = this.parsePostForm();
        if (data) {
            if (this.model) {
                this.model.save(data, {success: this.onSuccess});
            } else {
                this.collection.create(data, {wait: true, success: this.onSuccess});
            }
        }
    },

    onSuccess: function(model, response, options) {
        app.blogRouter.navigate('post/' + model.id, {trigger: true} );
    }

});