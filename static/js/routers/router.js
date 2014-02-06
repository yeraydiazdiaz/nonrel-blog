
var app = app || {};

var Workspace = Backbone.Router.extend({

    routes: {
        '': 'home',
        'post/*postID': 'viewPost'
    }

});
