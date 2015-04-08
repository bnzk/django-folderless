
(function($){
    // ready!
    $(function() {

        $('.inline-group').each(function(index, inline) {
            if ($(inline).find("fieldset .folderless_raw_id_field")) {
                //console.log("found inline with folderless fields!");
                //console.log($(inline).attr("id"));
                $(inline).find(".add-row").click(add_row_handler);
            };
        });

        function add_row_handler(event) {
            return;
            //alert("..");
            // depends on html structure, bad. but...
            inline = $(event.currentTarget).parent();
            //console.log(inline);
        }

            // check if we need to add folderless field functionality
    });

})(django.jQuery);
