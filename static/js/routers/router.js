
var Workspace = Backbone.Router.extend({

    routes: {
        'post/*postID': 'viewPost'
    },

    viewPost: function(param) {
        window.app.PostID = param ;
        window.app.BlogView.trigger('viewPost');
    }

});

app.BlogRouter = new Workspace();
Backbone.history.start();