// django autocomplete light to the rescue!

var folderless = folderless || {};
if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
    // If django.jQuery is already defined, use it.
    folderless.jQuery = django.jQuery;
} else {
    console.log("folderless field is only supported in django admin!");
}

// In addition to all of this, we must ensure that the global jQuery and $ are
// defined, because jqueryUI requires that. jQuery will only be undefined at
// this point if only we or django included it.
if (typeof jQuery === 'undefined') {
    jQuery = folderless.jQuery;
    $ = folderless.jQuery;
}
else {
    // jQuery IS still defined, which means someone else also included jQuery.
    // In this situation, we need to store the old jQuery in a
    // temp variable, set the global jQuery to our yl.jQuery, then let select2
    // set itself up. We restore the global jQuery to its original value in
    // jquery.post-setup.js.
    folderless_jquery_backup = jQuery.noConflict(true);
    jQuery = folderless.jQuery;
}