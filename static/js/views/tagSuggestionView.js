/**
 * TagSuggestionView renders a series of tags from the UniqueTagsCollection
 * that match begin with the letters being typed by the user.
 * It is created by the CreateEditPostView when the user types something in the
 * post-tags input field of the form.
 */

var app = app || {};

app.TagSuggestionsView = Backbone.View.extend({
    id: 'tag-suggestions',
    uniqueTagTemplate: _.template($('#uniqueTagTemplate').html()),

    /**
     * Render the view based on an array of elements. If nothing is passed
     * use all the models in the collection.
     * @param tags Optionally pass an array of tags.
     * @returns {app.TagSuggestionsView} The view for hierarchical rendering.
     */
    render: function(tags) {
        this.$el.html('');
        if (tags == undefined) {
            tags = this.collection.models;
        }
        _.each(tags, function(tag) {
            this.renderTagSuggestion(tag);
        }, this);
        return this;
    },

    /**
     * Render a single tag from a model.
     * @param tag An instance of a Tag model.
     */
    renderTagSuggestion: function(tag) {
        var json = tag.toJSON();
        json.cid = tag.cid;
        this.$el.append(this.uniqueTagTemplate( json ));
        // Add click handler on creation
        this.$el.find('#tag-'+tag.cid).click(this.onTagClick(this));
    },

    /**
     * Filter creates a list of non-repeated possible candidates based
     * on a previous array created from the current value in the field.
     * @param currentTagsArray Array created by left trimming the
     * current string in the field
     */
    filter: function(currentTagsArray) {
        // get list based on last element
        console.log(currentTagsArray);
        var lastElement = currentTagsArray.slice(-1);
        var previousTags = [];
        if (currentTagsArray.length > 1) {
            previousTags = currentTagsArray.slice(0, -1);
        }
        var candidate_tags = this.collection.filter(
            function(tag) {
                return tag.get('name').indexOf(lastElement) != -1;
            }
        )
        // take out the ones that are on the remaining array
        var notPresentTags = _.reject(candidate_tags,
            function(tag) {
                var result = _.contains(previousTags, tag.get('name'));
                return result;
            }
        );
        this.render(notPresentTags);
    },

    /**
     * Click handler on one of our tag buttons.
     * @param view An instance of this view to retrieve the collection.
     * @returns {Function} Anonymous function that triggers a custom event with
     * the name of the tag being clicked.
     */
    onTagClick: function(view) {
        return function() {
            var tag = view.collection.get(this.id.substr(4));
            view.trigger('clickedTag', tag.get('name'));
        }
    }
});