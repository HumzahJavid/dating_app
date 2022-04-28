$('#searchForm')
    .form({
        fields: {
            // search_type
            search_type: 'empty',
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
            if (settings.data["min_age"] == "") {
                settings.data["min_age"] = 18
            }
            if (settings.data["max_age"] == "") {
                settings.data["max_age"] = 64
            }

            console.log(settings.data)
            return settings
        },
        onResponse: function (response) {
            console.log(response);
            return response
        },
    });
