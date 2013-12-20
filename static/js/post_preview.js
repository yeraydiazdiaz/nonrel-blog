/**
	post_preview.js
	
	Enables preview of the post form.
 */
 
 $(document).ready(function() {
	 $("#preview").click(
	 	function() {
	 		var title = $("#post-title").val();
	 		var text = $("#post-text").val();
	 		$("#post-preview").css( "padding", "1em" );
	 		$("#post-preview").html( "<h2>"+ title +"</h2><p>"+ text +"</p><hr/>" );
	 		$("#submit").removeAttr( "disabled" );
	 	}
	 ); // end click
});