/**
 * Router for Nonrel-blog.
 */

var app = app || {};

var Workspace = Backbone.Router.extend({

    routes: {
        '': 'home',
        'post/*postID/edit': 'editPost',
        'post/*postID': 'viewPost',
        'tag/*tag': 'tag',
        'create_post': 'createPost',
        'search/*terms': 'search',
        'user/*username': 'user'
    }

});
