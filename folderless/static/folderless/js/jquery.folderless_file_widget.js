
// TODO: implement uploader, remove, onchange!

(function($){
	$.fn.folderless_file_widget = function()
	{
		this.each(function(){
			var _self = $(this);
            var browse_button = _self.find(".folderless_browser");
            var upload_button = _self.find(".folderless_uploader");
            var upload_info = _self.find(".folderless_upload_info");
            var remove_button = _self.find(".folderless_remove");
            var edit_button = _self.find(".folderless_edit");
            var unknown_img = _self.find(".folderless_unknown");
            var raw_id_field = _self.find(".folderless_raw_id_field input");
            var label = _self.find(".folderless_file_label");
            var thumb = _self.find(".folderless_thumb");
            var file_link = _self.find(".folderless_file_link");
            var file_input = _self.find(".folderless_fileinput");

            var ajax_request = false;

            var init = function() {
                // cleanup from rawidfield
                _self.find(".add-another").hide(0);
                // return from browse
                raw_id_field.change(raw_id_changed);
                // uploader
                upload_button.click(function(e) { e.preventDefault(); file_input.click(); });
                file_input.fileupload({
                    dataType: 'json',
                    replaceFileInput: false,
                    sequentialUploads: true,
                    add: function(e, data) {
                        upload_info.show(0);
                        browse_button.hide(0);
                        upload_button.hide(0);
                        remove_file();
                        data.submit();
                    },
                    done: function (e, data) {
                        update_file_info_n_interface(data.result);
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        upload_info.find("span").html(progress + "%")
                    }
                });
                remove_button.click(remove_file);
            }

            var update_file_info_n_interface = function(data) {
                thumb.attr("src", data.thumbnail_field);
                thumb.attr("alt", data.label);
                label.html(data.label);
                raw_id_field.val(data.id);
                file_link.attr("href", data.file_url);
                edit_button.show(0);
                edit_button.attr("href", data.edit_url);
                remove_button.show(0);
                browse_button.show(0);
                upload_button.show(0);
                upload_info.hide(0);
            }

            var raw_id_changed = function() {
                var data = {"file_id": raw_id_field.val()};
                var url = browse_button.attr("data-info-url");
                if (ajax_request) {
                    ajax_request.abort();
                }
                ajax_request = $.get(url, data,
                    function(data, textStatus, xhr) {
                        ajax_request = false;
                        update_file_info_n_interface(data);
                    });

            }

            var remove_file = function() {
                raw_id_field.val("");
                thumb.attr("src", unknown_img.attr("src"));
                thumb.attr("alt", unknown_img.attr("alt"));
                file_link.removeAttr("href");
                label.html("");

                remove_button.hide(0);
                edit_button.hide(0);
            }


            init();

		});
	}
})(jQuery);
