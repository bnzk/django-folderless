
// TODO: implement uploader, remove, onchange!

(function($){
	$.fn.folderless_change_list = function()
	{
		this.each(function(){
			var _self = $(this);
            var upload_button = _self.find(".folderless_uploader");
            var upload_info = _self.find(".folderless_upload_info");
            var files_total = 0;
            var files_uploaded = 0;
            var files_upload_error= 0;
            var file_input = _self.find(".folderless_fileinput");


            var init = function() {
                // uploader instead of classic "add"
                upload_button.click(function(e) { e.preventDefault(); file_input.click(); });
                file_input.fileupload({
                    dataType: 'json',
                    replaceFileInput: false,
                    sequentialUploads: true,
                    add: function(e, data) {
                        upload_info.show(0  );
                        files_total += 1;
                        upload_info.find(".total").html(files_total);
                        data.submit();
                    },
                    send: function(e, data) {

                    },
                    fail: function(e, data) {
                        files_upload_error += 1;
                        upload_info.find(".upload_errors").show(0).find("span").html(files_upload_error);
                    },
                    done: function (e, data) {
                        files_uploaded += 1;
                        upload_info.find(".uploaded").html(files_uploaded);
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        upload_info.find(".percent").html(progress + "%");
                        if (data.loaded / data.total == 1) {
                            upload_info.find(".status").html("processing...")
                            // TODO: why does it trigger a "fail" if we dont delay this?!
                            setTimeout(function() { document.location.reload(); }, 100);
                        }
                    }
                });
            }

            init();

		});
	}
})(jQuery);
