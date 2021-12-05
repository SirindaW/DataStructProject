/* Script for filter query */

function href_query_filter(parameter, value) {
    // type is query set key, filter is new query value to replace
    // Get current url
    var url = window.location.href;

    // Create new queryset incase of query never existed
    var qs = [parameter, "=", value].join("");
    var result;
    if (url.indexOf("?") > -1) {
        // check if query has happened before
        if (url.includes(parameter)) {
            // already has existed type in queryset
            var regex = new RegExp("(" + parameter + "=)[^&]+");
            result = url.replace(regex, "$1" + value);
            //result = url.replace(type_key, '$1' + filter);
        } else {
            // else this type has never existed
            result = [url, "&", qs].join("");
        }
    } else {
        var result = ["?", qs].join("");
    }
    id = [value, "-filter"].join("");
    //alert(id);
    document.getElementById(id).href = result;
}

function render_checkboxes_states() {
    /* load checkboxes states from sessionStorage and change each checkboxes states corresposing to the stored state */
    storedStates = JSON.parse(sessionStorage.checkboxesStates)

    for (var key in Object(storedStates)) {
        checkbox = document.getElementById(key)
            // console.log(checkbox.id, checkbox.checked, storedStates[key])
        checkbox.checked = storedStates[key]

    }
}

function clear_collection_checkboxes_states() {

    // retrieving the data from sessionStorage
    storedStates = JSON.parse(sessionStorage.checkboxesStates)
    states = {}
    for (var key in Object(storedStates)) {
        states[key] = false;
    }

    // store back the data
    sessionStorage.setItem('checkboxesStates', JSON.stringify(states))


    // reload the checkboxes states
    render_checkboxes_states()

}

function clear_all_checkbox_filter() {
    clear_collection_checkboxes_states()
}

function query_filter_cases_href() {
    /* load checkboxes states from sessionStorage and return query for filter */
    filter_checked = []
    states = JSON.parse(sessionStorage.checkboxesStates)

    for (var key in states) {
        if (states[key] == true) {
            filter_checked.push(key)
        }
    }

    // Read from checkboxes
    // var allCollections = document.getElementById('collection-form').children
    // for (let i = 0; i < allCollections.length; i++) {
    //     checkbox = allCollections[i].children[0];
    //     if (checkbox.checked == true) {
    //         filter_checked.push(checkbox.id);
    //     }
    // }


    console.log(filter_checked);

    var current_url = window.location.href;

    params = new URLSearchParams(current_url.split('?')[1]);
    params.delete('collection');

    for (var i in filter_checked) {
        params.append('collection', filter_checked[i]);
    }

    console.log(params.toString());

    var url_with_query = current_url.split('?')[0] + '?' + params.toString();
    return url_with_query
}

function query_collection_filter() {
    /* reload current page with current filter states */
    var url_with_query = query_filter_cases_href();
    window.location.replace(url_with_query);

    // new_url = 
    // window.location.replace('/cases/?collection=squidgame&collection=coke')

}

function filter_checkbox_collection_onchange() {

    var allCollections = document.getElementById('collection-form').children
    states = {}
    for (let i = 0; i < allCollections.length; i++) {
        chxbx = allCollections[i].children[0];
        state = chxbx.checked;
        states[chxbx.id] = state;
        if (state == true) {}
    }

    // store data to sessionStorage
    sessionStorage.setItem('checkboxesStates', JSON.stringify(states))

    form = document.getElementById('collection-form')
        // form.submit()

    // window.location.replace('/cases/?model=iphone13promax');
    query_collection_filter()


}

function filter_checkbox_onchange() {
    // alert('hello');
}