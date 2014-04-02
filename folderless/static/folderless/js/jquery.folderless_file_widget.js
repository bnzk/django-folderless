
// TODO: implement uploader, remove, onchange!

(function($){
	$.fn.folderless_file_widget = function()
	{
		this.each(function(){
			var _self = $(this);
            var uploader = _self.find(".folderless_uploader");
            var raw_id_field = _self.find(".folderless_raw_id_field input");
            var label = _self.find(".folderless_label");
            var thumb = _self.find(".folderless_thumb");
            var file_link = _self.find(".folderless_file_link");

            var init = function() {
                // cleanup from rawidfield
                _self.find(".add-another").hide(0);
                raw_id_field.change(raw_id_changed);
            }

            var file_selected = function() {
                console.log("file selected - upload!");
            }

            var raw_id_changed = function() {
                console.log("file changed. update things!");
                console.log(this);
                console.log(_self);
            }

            init();

		});
	}
})(jQuery);
