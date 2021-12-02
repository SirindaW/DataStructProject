/* Script for filter query */

function href_query_filter(parameter, value) { // type is query set key, filter is new query value to replace
    // Get current url
    var url = window.location.href;

    // Create new queryset incase of query never existed
    var qs = [parameter, '=', value].join('');
    var result;
    if (url.indexOf('?') > -1) { // check if query has happened before
        if (url.includes(parameter)) {
            // already has existed type in queryset
            var regex = new RegExp('(' + parameter + '=)[^\&]+');
            result = url.replace(regex, '$1' + value);
            //result = url.replace(type_key, '$1' + filter);
        } else {
            // else this type has never existed
            result = [url, '&', qs].join('');
        }

    } else {
        var result = ['?', qs].join('');

    }
    id = [value, '-filter'].join('')
        //alert(id);
    document.getElementById(id).href = result

}