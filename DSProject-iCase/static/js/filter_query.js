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

    /* For price checkboxes */
    storedPriceFilterState = JSON.parse(sessionStorage.priceCheckboxesStates)
    if (storedPriceFilterState !== '') {
        id = Object.keys(storedPriceFilterState)[0]
        checkbox = document.getElementById(id)
        checkbox.checked = true
    } else {
        price_checkboxes = document.getElementsByClassName('price-checkbox')
        for (var i = 0; i < price_checkboxes.length; i++) {
            price_checkboxes[i].checked = false
        }
        console.log('something')
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

function clear_price_checkboxes_states() {
    sessionStorage.setItem('priceCheckboxesStates', JSON.stringify(''))
    render_checkboxes_states()
        // var price_checkboxes = document.getElementsByClassName('price-checkbox')
        // for (var i = 0; i < price_checkboxes; i++) {
        //     price_checkboxes[i].checked = false
        //     console.log(price_checkboxes[i])
        // }
}

function clear_all_checkbox_filter() {
    clear_collection_checkboxes_states()
}

/* Generate href with query string for stored filter checkboxes states */
function query_filter_cases_href() {
    /* load checkboxes states from sessionStorage and return query for filter */
    filter_checked = []
    states = JSON.parse(sessionStorage.checkboxesStates)

    for (var key in states) {
        if (states[key] == true) {
            filter_checked.push(key)
        }
    }

    console.log(filter_checked);

    var current_url = window.location.href;

    params = new URLSearchParams(current_url.split('?')[1]);
    params.delete('collection');

    for (var i in filter_checked) {
        params.append('collection', filter_checked[i]);
    }

    /* price filter */
    price_range = JSON.parse(sessionStorage.getItem('priceCheckboxesStates'))
    params.delete('price');
    console.log(price_range)
    if (price_range !== '') {
        console.log('obj', Object.keys(price_range)[0])
        var key = Object.keys(price_range)[0]
        var value = price_range[key]
        params.append('price', value)
    }


    console.log(params.toString());

    var url_with_query = current_url.split('?')[0] + '?' + params.toString();
    return url_with_query
}

/* Making query by sending request to server with query string. */
function query_filter() {
    /* reload current page with current filter states */
    var url_with_query = query_filter_cases_href();
    window.location.replace(url_with_query);


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
    query_filter()
}

/* Read and store the states of price-checkboxes in sessionStorage on change */
function filter_checkbox_price_onchange() {
    // var prices = document.getElementsByClassName('price-checkbox')
    prices = document.getElementsByClassName('price-checkbox')

    for (var i = 0; i < prices.length; i++) {
        if (prices[i].checked) {
            console.log("THIS", prices[i].id)
            var id = prices[i].id
            id = String(id)
            state = {}
            state[id] = prices[i].dataset.priceRange
            sessionStorage.setItem('priceCheckboxesStates', JSON.stringify(state))
            return
        }
    }
    /* no checkboxes checked , novalues*/
    sessionStorage.setItem('priceCheckboxesStates', JSON.stringify(''))

    // console.log(sessionStorage.getItem('pricesCheckboxesStates'))
    // Stores the state to sessionStorage
}

/* Query the filter with checked price */
function query_price_filter() {
    // Read from sessionStorage
    state = JSON.parse(sessionStorage.getItem('priceCheckboxesStates'))
    x = query_filter_cases_href()
    console.log("..", state)
    console.log(x)
}

/* Encapsulate the EventListener Fuction */
function priceFilterEventListener() {
    filter_checkbox_price_onchange()
    console.log('this is in the memory', sessionStorage.getItem('priceCheckboxesStates'))
    query_price_filter()
    query_filter()
}