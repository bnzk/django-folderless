

function dismissRelatedFolderlessLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        elem.value = chosenId;
    }
    // the reason for this custom thing!
    folderless.jQuery(elem).trigger("change");
    win.close();
}
