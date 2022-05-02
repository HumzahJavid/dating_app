$('#editForm')
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
            password: {
                identifier: 'password',
                optional: true,
                rules: [
                    {
                        type: 'empty',
                    }
                ]
            },
            name: {
                identifier: 'name',
                optional: true,
                rules: [
                    {
                        type: 'empty',
                    }
                ]
            },
            age: {
                identifier: 'age',
                optional: true,
                rules: [
                    {
                        type: 'integer[18..64]',
                    }
                ]
            },
        }
    })

    .api({
        url: '/me',
        method: 'PUT',
        serializeForm: true,
        onResponse: function (response) {
            console.log("response = ");
            console.log(response);
            return response
        },
        onSuccess: function (response, element, xhr) {
            console.log("response = ");
            console.log(response);
            console.log("element = ");
            console.log(element);
            console.log("xhr = ");
            console.log(xhr);
            // $('body').toast({
            //     class: 'success',
            //     message: `${response.message} ${response.email}`,
            //     pauseOnHover: false,
            //     showProgress: 'top'
            // });
        },
    });
