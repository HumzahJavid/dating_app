$('#searchForm')
    .form({
        fields: {
            email: 'email',
            // name: '',
            min_age: 'integer[18..64]',
            min_age: 'different[max_age]',
            max_age: 'integer[18..64]',
        }
    })
    .api({
        url: '/search',
        method: 'GET',
        serializeForm: true,
        beforeSend: function (settings) {
            console.log(settings)
            return settings
        },
        onResponse: function (response) {
            console.log(response);
            return response
        },
    });
