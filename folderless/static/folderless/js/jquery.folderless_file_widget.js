
// TODO: implement uploader, remove, onchange!

(function($){
	$.fn.folderless_file_widget = function()
	{
		this.each(function(){
			var _self = $(this);
            var uploader = _self.find(".folderless_uploader");
            var label = _self.find(".folderless_label");
            var thumb = _self.find(".folderless_thumb");
            var file_link = _self.find(".folderless_file_link");

            var init = function() {
                _self.find(".add-another").hide(0);
            }

            var file_selected = function() {
                console.log("file selected!");
            }

            var raw_id_changed = function() {
                console.log("file changed!");
                console.log(this);
                console.log(_self);
            }

            init();

		});
	}
})(jQuery);
