$('#searchForm')
    .form({
        fields: {
            email: {
                identifier: 'email',
                optional: true,
                rules: [
                    {
                        type: 'email',
                    }
                ]
            },
            min_age: {
                identifier: 'min_age',
                // optional is implied with depends (non empty field)
                // optional: true,
                depends: 'max_age',
                rules: [
                    {
                        type: 'integer[18..64]',
                    },
                    {
                        type: 'different[max_age]'
                    }
                ]
            },
            max_age: {
                identifier: 'max_age',
                depends: 'min_age',
                rules: [
                    {
                        type: 'integer[18..64]',
                    },
                    {
                        type: 'different[min_age]'
                    }
                ]
            },
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
