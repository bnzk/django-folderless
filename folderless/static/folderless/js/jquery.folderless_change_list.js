
// TODO: implement uploader, remove, onchange!

(function($){
	$.fn.folderless_change_list = function()
	{
		this.each(function(){
			var _self = $(this);
            var upload_button = _self.find(".folderless_uploader");
            var upload_info = _self.find(".folderless_upload_info");
            var file_input = _self.find(".folderless_fileinput");


            var init = function() {
                // uploader instead of classic "add"
                upload_button.click(function(e) { e.preventDefault(); file_input.click(); });
                file_input.fileupload({
                    dataType: 'json',
                    replaceFileInput: false,
                    sequentialUploads: true,
                    add: function(e, data) {
                        upload_info.show(0);
                        data.submit();
                    },
                    done: function (e, data) {
                        //document.location.reload();
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        upload_info.find("span").html(progress + "%");
                        if (data.loaded / data.total == 1) {
                            upload_info.find("span").html(progress + "% - processing...");
                            document.location.reload();
                        }
                    }
                });
            }

            init();

		});
	}
})(jQuery);
