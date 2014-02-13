/**
 * PostView represents a Post with all the available information.
 * It also is the only place on which to post comments from.
 * Comments are *not* handled by Backbone models but rather by manually
 * invoking $.ajax to a specific endpoint. This is because the comments in the
 * back-end are not standalone models but are embedded into the Posts.
 */

var app = app || {};

app.PostView = Backbone.View.extend({
    tagName: 'div',
    className: 'post-list',
    template: _.template($('#postTemplate').html()),
    formErrorTemplate: _.template($('#formErrorTemplate').html()),
    confirmDeletionTemplate: _.template($('#confirmDeletionTemplate').html()),

    events: {
        'click #comment-submit': 'submitComment',
        'click #delete-post': 'confirmDelete'
    },

    initialize: function() {
        this.listenTo(this.model, 'sync', this.render);
    },

    /**
     * Rendering of the view is simply passing the model to the template
     * except we're doing some rudimentary parsing of carriage returns into P tags.
     * @returns {app.PostView}
     */
    render: function() {
        var json = this.model.toJSON()
        json.text = this.replaceNewLinesWithPs(json.text);
        this.$el.html( this.template( json ) );
        return this;
    },

    /**
     * Replaces carriage returns for P tags.
     * @param raw_template HTML from the template.
     * @returns {string} HTML with P tags.
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
     * Scans a field on the comment form and adds an error message if it fails
     * a verification.
     * @param field A jQuery object of the field.
     * @returns {*} The value or false if it did not pass.
     */
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

    /**
     * Auxiliary function to validate an email.
     * @param email String to be matched against an email.
     * @returns {boolean} The result of the match.
     */
    validateEmail: function (email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    },

    /**
     * Takes the comment form and validates all fields, returning an object
     * with the necessary structure or false.
     * @returns {*} A correct object or false.
     */
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

    /**
     * If the validation succeeds perform the AJAX query.
     */
    submitComment: function() {
        this.$el.find('.alert').remove();
        this.toggleCommentSubmitButtton();
        data = this.parseCommentForm();
        if (data != false) {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader('X-CSRFToken', app.csrf_token);
                }
            });
            $.ajax({
                type: "POST",
                url: '/api/posts/' + this.model.id + '/comments',
                data: data,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                complete: this.onCommentAjaxComplete(this)
            });
        }
    },

    /**
     * Query result handler, if the comment was successfully posted we refetch
     * the model to show the user the current state of the post.
     * @param view This PostView to access the model to fetch.
     * @returns {Function} An anonymous function that recieves a jqXHR object and a result.
     */
    onCommentAjaxComplete: function(view) {
        return function(jqXHR, textStatus) {
            if (textStatus == 'error') {
                alert(jqXHR.responseText);
            } else {
                view.model.fetch();
            }
        }
    },

    /**
     * Shows a confirmation dialog if the user clicks Delete Post.
     * Sets up the jQuery click handlers for either option.
     */
    confirmDelete: function() {
        this.$el.html(this.confirmDeletionTemplate() + this.$el.html());
        $(".alert").alert()
        $('#delete-no').click( function() {
            $(".alert").alert('close');
        });
        $('#delete-yes').click( function(view) {
            return function() {
                $(".alert").alert('close');
                view.deletePost();
            }
        }(this));
    },

    /**
     * Destroys the model and navigates to the home screen after confirmation.
     */
    deletePost: function() {
        this.model.destroy( {
            success: function() {
                app.blogCollection.fetch();
            }
        });
        app.blogRouter.navigate('', {trigger: true} );
    },

    /**
     * Adds/removes the disabled attribute on the submit comment button.
     */
    toggleCommentSubmitButtton: function() {
        if ($('#comment-submit').attr('disabled') == undefined) {
            $('#comment-submit').attr('disabled', 'disabled');
        } else {
            $('#comment-submit').removeAttr('disabled');
        }
    },

});