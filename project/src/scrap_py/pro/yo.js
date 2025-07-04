const leboncoin = require('leboncoin-api');
var search = new leboncoin.Search()
    .setPage(1)
    .setQuery("renove")
    .setFilter(leboncoin.FILTERS.PARTICULIER)
    .setCategory("locations")
    .setRegion("ile_de_france")
    .addSearchExtra("price", {min: 1500, max: 2000}) // will add a range of price
    .addSearchExtra('furnished', ["1", "Non meublé"]); // will add enums for Meublé and Non meublé

search.run().then(function (data) {
    console.log(data.page); // the current page
    console.log(data.nbResult); // the number of results for this search
    console.log(data.results); // the array of results
    data.results[0].getDetails().then(function (details) {
        console.log(details); // the item 0 with more data such as description, all images, author, ...
    }, function (err) {
        console.error(err);
    });
    data.results[0].getPhoneNumber().then(function (phoneNumer) {
        console.log(phoneNumer); // the phone number of the author if available
    }, function (err) {
        console.error(err); // if the phone number is not available or not parsable (image -> string)
    });
}, function (err) {
    console.error(err);
});
