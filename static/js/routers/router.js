
var app = app || {};

var Workspace = Backbone.Router.extend({

    routes: {
        '': 'home',
        'post/*postID': 'viewPost'
    }

});

app.BlogRouter = new Workspace();
Backbone.history.start();