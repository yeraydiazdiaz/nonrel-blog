
var app = app || {};

var Workspace = Backbone.Router.extend({

    routes: {
        '': 'home',
        'post/*postID': 'viewPost',
        'tag/*tag': 'tag',
        'create_post': 'createPost'
    }

});
