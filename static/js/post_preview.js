/**
    post_preview.js

    Enables preview of the post form.
 */
 
 function preview_post() {
            var title = $("#post-title").val();
            var text = $("#post-text").val();
            text = "<p>" + text.replace(/\n/g, "</p><p>") + "</p>";
            $("#post-preview").css( "padding", "1em" );
            $("#post-preview").html( "<h2>"+ title +"</h2><p>"+ text +"</p><hr/>" );
            $("#submit").removeAttr( "disabled" );
        }
 
 $(document).ready(function() {
     $("#preview").show();
     $("#submit").attr("disabled", "disabled");
     $("#preview").click( function() {
            var tags = $("#post-tags").val();
            $("#post-tags").val( tags.replace(/,./, " ") );
            preview_post();
         }
     ); // end click
});