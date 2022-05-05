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
            $('body').append("<h2> Search results </h2>");

            for (let i = 0; i < response.length; i++) {
                card_name = response["data"][i]["name"]
                card_age = response["data"][i]["age"]
                card_gender = response["data"][i]["gender"]
                card_email = response["data"][i]["email"]
                card = create_card(card_name, card_age, card_gender, card_email)
                $('body').append(card);
            }
        },
    });


function create_card(name, age, gender, email) {
    console.log("creating card with email" + email)
    picture_file = "/static/images/image.png"
    if (gender == "male") {
        picture_file = "/static/images/steve.jpg"
        image_str = ' <img src = "/static/images/steve.jpg">'
    } else if (gender == "female") {
        picture_file = "/static/images/stevie.jpg"
        // image_str = '<img src = "/static/images/stevie.jpg" data-email="' + email + '">'
    }
    image_str = ` <img class = "imageChat" src = "${picture_file}" data-email = "${email}">`

    str = '' + '<div class="ui card">'
        + '<div class="image">'
        + image_str
        + '</div>'
        // + '<div> result </div >'
        + '<div class="content">'
        + ' <a class="header">' + name + '</a>'
        + '  <div class= "description">'

        + '   <div class="card_age">'
        + '    Age: ' + age
        + '   </div>'

        + '   <div class="card_gender">'
        + '    Gender: ' + gender
        + '   </div>'

        + '  </div>' // description
        + '</div>' // content
        + '</div>' // ui card
    return str
}

$(document).on('click', '.imageChat', function (e) {
    email = e.currentTarget.dataset["email"]
    console.log("click image via doc for " + email);
    // post to fastapi to start a chat
    // senders email from sessionstorage
    // recepient email from this method
    // $.post(this.href, function (data) {
    //     $("#someContainer").html(data);
    // })

});
