        $('.ui.dropdown')
            .dropdown();
        $(document).on('click', '#loginButton', function () {
            $('#loginModal')
                .modal({
                    blurring: false
                })
                .modal('setting', 'transition', "scale")
                .modal('show')
        });

        $(document).on('click', '#logoutButton', function () {
            $('#logoutButton')
                .api({
                    url: '/api/user/logout',
                    method: 'POST',
                    onResponse: function (response) {
                        console.log("logout response = ");
                        console.log(response);

                    },
                    onSuccess: function (response, element, xhr) {
                        // valid response and response.success = true
                        console.log("xhr = ");
                        console.log(xhr);
                        $('body').toast({
                            class: 'success',
                            message: `${response.message}`,
                            pauseOnHover: false,
                            showProgress: 'top'
                        });
                        sessionStorage.removeItem('loggedIn');
                        sessionStorage.removeItem('user');
                        swap_buttons();
                    },
                });
        });
        $('#loginForm .submit.button')
            .api({
                url: '/api/user/login',
                method: 'POST',
                serializeForm: true,
                beforeSend: function (settings) {
                    console.log(settings)
                    return settings
                },
                onResponse: function (response) {
                    console.log("RESPONSE = ");
                    console.log(response);
                    $('#loginModal').modal('hide')
                    return response
                },
                onSuccess: function (response, element, xhr) {
                    // valid response and response.success = true
                    console.log("response = ");
                    console.log(response);
                    console.log("element = ");
                    console.log(element);
                    console.log("xhr = ");
                    console.log(xhr);
                    $('#loginModal').modal('hide')
                    $('body').toast({
                        class: 'success',
                        message: `${response.message}`,
                        pauseOnHover: false,
                        showProgress: 'top'
                    });
                    sessionStorage.setItem('loggedIn', true)
                    sessionStorage.setItem('user', response.email)
                    console.log("deactivating login (and reg)")
                    swap_buttons()
                },
                onError(errorMessage, element, xhr) {
                    console.log("errorMessage = ");
                    console.log(errorMessage);
                    console.log("element = ");
                    console.log(element);
                    console.log("xhr = ");
                    console.log(xhr);
                    response = xhr.responseJSON
                    $('#loginModal').modal('hide')
                    $('body').toast({
                        class: 'error',
                        message: `${response.message}`,
                        pauseOnHover: false,
                        showProgress: 'top'
                    });
                },
            });

        $('#registrationForm')
            .form({
                fields: {
                    match: {
                        identifier: 'confirmPassword',
                        rules: [
                            {
                                type: 'match[password]',
                                prompt: 'Please ensure the passwords match'
                            }
                        ]
                    }
                }
            })
            .api({
                url: '/api/user/register',
                method: 'POST',
                serializeForm: true,
                beforeSend: function (settings) {
                    console.log(settings)
                    return settings
                },
                onResponse: function (response) {
                    console.log("response = ");
                    console.log(response);
                    $('#registrationModal').modal('hide')
                    return response
                },
                onSuccess: function (response, element, xhr) {
                    // valid response and response.success = true
                    console.log("response = ");
                    console.log(response);
                    console.log("element = ");
                    console.log(element);
                    console.log("xhr = ");
                    console.log(xhr);
                    $('#registrationModal').modal('hide')
                    $('body').toast({
                        class: 'success',
                        message: `${response.message} ${response.email}`,
                        pauseOnHover: false,
                        showProgress: 'top'
                    });
                    $('#loginModal').modal('show')
                },
                onError(errorMessage, element, xhr) {
                    console.log("errorMessage = ");
                    console.log(errorMessage);
                    console.log("element = ");
                    console.log(element);
                    console.log("xhr = ");
                    console.log(xhr);
                    response = xhr.responseJSON
                    $('body').toast({
                        class: 'error',
                        message: `${response.message} ${response.email}`,
                        pauseOnHover: false,
                        showProgress: 'top'
                    });
                },
            });

        $(document).on('click', '#registrationLink', function () {
            $('#registrationModal')
                .modal({
                    blurring: true
                })
                .modal('setting', 'transition', "scale")
                .modal('show')
        });
        function swap_buttons() {
            console.log("swapping buttons");
            if (sessionStorage.getItem('loggedIn')) {
                hidden_element = $('#logoutButton');
                visible_element = $('#loginButton');
            } else {
                hidden_element = $('#loginButton');
                visible_element = $('#logoutButton');
            }
            hidden_element.show();
            visible_element.hide();
        }

        window.addEventListener("beforeunload", (ev) => {
            $.ajax({
                type: "POST",
                url: "/api/user/logout"
            });
        });
        window.onload = swap_buttons();//$('#logoutButton').hide();
