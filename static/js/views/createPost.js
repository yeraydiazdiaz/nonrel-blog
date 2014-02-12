/**
 * CreateEditPostView handles the form for creating and editing posts.
 * Also allows previewing the post before submitting the form.
 * @type {app|*|app|*|{}|{}}
 */

var app = app || {};

app.CreateEditPostView = Backbone.View.extend({
    template: _.template($('#postFormTemplate').html()),
    formErrorTemplate: _.template($('#formErrorTemplate').html()),
    postTemplate: _.template($('#postTemplate').html()),

    events: {
        'click #preview-post': 'previewPost',
        'click #submit-post': 'submitPost',
        'keyup #post-tags': 'getUniqueTags'
    },

    /**
     * Initialize the view by setting the mode, Edit or Create.
     * @param options Hash of options that include mode.
     */
    initialize: function(options) {
        this.mode = options.mode;
    },

    /**
     * Rendering depends on if we're editing a post. If we are populate the form with
     * the necessary data.
     * @returns {app.CreateEditPostView} An instace of the view for parent view to render.
     */
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

    /**
     * Quick function to replace new lines with P tags in templates when previewing.
     * @param raw_template The result of rendering a model through the template.
     * @returns {string} A pseudo-HTML markup with new lines removed.
     */
    replaceNewLinesWithPs: function(raw_template) {
        var added_ps = '<p>'+raw_template.replace(/\n+/g, '</p><p>')
        if (added_ps.substr(-4) != '</p>') {
            return added_ps + '</p>';
        }else{
            return added_ps;
        }
    },

    /**
     * Simple validation whereby if a model is empty we display an alert.
     * @param field Form field to validate.
     * @returns {*} The value of the field or false if it was empty.
     */
    validateField: function(field) {
        var value = field.val();
        if (value != '') {
            return value;
        } else {
            field.after(this.formErrorTemplate({error_msg: 'This field is required'}));
            return false;
        }
    },

    /**
     * Simple parsing function returning false if any of the fields is empty
     * or an object with properly named attributes to be used.
     * @returns {*} A well-formed object or false if any fields are empty.
     */
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

    /**
     * Function to preview the current data being introduced, uses the post template and
     * passes optional elements. Some of the logic is in the postTemplate to skip certain
     * sections.
     */
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
            data.text = this.replaceNewLinesWithPs(data.text)
            this.$('#post-preview').html( this.postTemplate(data) );
        }
    },

    /**
     * Handles submission of the form, patching the model or creating a model on the collection
     * depending if we're editing or creating.
     */
    submitPost: function() {
        this.$el.find('.alert').remove();
        this.toggleButtons();
        var data = this.parsePostForm();
        if (data) {
            if (this.model) {
                // PATCH requests are rejected by the development server but not by the prod server.
                this.model.save(data, {patch: true, success: this.onSuccess, error: this.onError});
            } else {
                this.collection.create(data, {wait: true, success: this.onSuccess, error: this.onError});
            }
        }
    },

    /**
     * Toggle buttons function to avoid multiple submission requests.
     */
    toggleButtons: function() {
        if ($('#submit-post').attr('disabled') == undefined) {
            $('#submit-post').attr('disabled', 'disabled');
            $('#preview-post').attr('disabled', 'disabled');
        } else {
            $('#submit-post').removeAttr('disabled');
            $('#preview-post').removeAttr('disabled');
        }
    },

    /**
     * Success handler on the submission request.
     * @param model Model submitted.
     * @param response Response from the server.
     * @param options Options.
     */
    onSuccess: function(model, response, options) {
        app.blogRouter.navigate('post/' + model.id, {trigger: true} );
    },

    /**
     * Error handler on the submission request.
     * @param model Model submitted.
     * @param response Response from the server.
     * @param options Options.
     */
    onError: function(model, response, options) {
        alert(response.responseText);
    },

    /**
     * Initializes the tag autocomplete system and fires updates on it.
     * if the collection and the view are in place simply call filter on the view.
     * Otherwise fetch on the uniqueTagsCollection and create the view.
     */
    getUniqueTags: function() {
        if (this.tagSuggestionsView != undefined) {
            this.tagSuggestionsView.filter($('#post-tags').val().trimLeft().split(' '));
        } else {
            app.uniqueTagsCollection.fetch({success: this.onTagFetchSuccess(this), error: this.onError});
        }
    },

    /**
     * Handler of a successful fetch on the uniqueTags collection, creating the TagSuggestionView.
     * @param view Instance of this view to access its methods.
     * @returns {Function} Anonymous function that calls the view's method.
     */
    onTagFetchSuccess: function(view) {
        return function(collection, response, options) {
            view.createTagSuggestionView()
        }
    },

    /**
     * Function to create the view and add its render result to this view.
     */
    createTagSuggestionView: function() {
        this.tagSuggestionsView = new app.TagSuggestionsView({collection: app.uniqueTagsCollection});
        var split = $('#post-tags').val().trimLeft().split(' ');
        this.tagSuggestionsView.filter(split);
        $('#post-tags').after(this.tagSuggestionsView.el);
        // listen to the custom event to trigger autocompletion
        this.listenTo(this.tagSuggestionsView, 'clickedTag', this.autocompleteTag);
    },

    /**
     * Function to autocomplete based on the clicked tag.
     * Creates an array from the current value of the field and adds the new one at the end.
     * @param tag Name of the tag to be added based on the information from the tagSuggestionView.
     */
    autocompleteTag: function(tag) {
        var currentValue = $('#post-tags').val();
        var elements = currentValue.split(' ');
        elements[elements.length-1] = tag;
        $('#post-tags').val(elements.join(' '));
        $('#post-tags').focus();
    }

});