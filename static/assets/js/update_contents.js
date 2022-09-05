function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function add_item(item, redirect_url, filter_checkbox) {
    $(function () {
        if (filter_checkbox) {
            input_HTML = `<input type="text" id="item-value" class="swal2-input" placeholder="${item}">
                            <input type="checkbox" id="is_filterable" class="filled-in" checked="">
                            <label for="basic_checkbox_2"> Include as a filter option</label>`
        } else {
            input_HTML = `<input type="text" id="item-value" class="swal2-input" placeholder="${item}">`
        }
        Swal.fire({
            title: 'Add new ' + item,
            html: input_HTML,
            iconHtml: '<i class="material-icons" style="color: #3fc3ee; ">add_to_photos</i>',
            confirmButtonText: 'Save',
            focusConfirm: false,
            icon: 'info',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            preConfirm: () => {
                const value = Swal.getPopup().querySelector('#item-value').value
                var is_filterable = false
                if (filter_checkbox) {
                    is_filterable = Swal.getPopup().querySelector('#is_filterable').value
                }
                if (!value) {
                    Swal.showValidationMessage(`Please enter a value`)
                }
                return {value: value, is_filterable: is_filterable}
            }
        }).then((result) => {
            $.ajax({
                url: "/api/v1/content/create-" + item + "/",
                type: 'post',
                contentType: 'application/json',
                data: `{
                            "title": "${result.value.value.trim()}",
                            "value": "${result.value.value.trim()}",
                            "exclude_from_filter": ${result.value.is_filterable}
                        }`,
                success: function (data) {
                    console.log("success");
                    console.log(data);
                    Swal.fire(
                        'Created!',
                        `New ${item} has been created.`,
                        'success'
                    )
                    setTimeout(function () {
                        window.location = redirect_url;
                    }, 1200)
                },
                error: function (data) {
                    Swal.fire(
                        'Failed',
                        'Failed to create new ' + item + ' !!',
                        'error'
                    )
                    console.log("error");
                    console.log(data);
                },
                cache: false,
                processData: false,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

        })
    })
}

function update_item(item, redirect_url, filter_checkbox, lkp_id, value, is_filterable_value) {
    $(function () {
        if (filter_checkbox) {
            alert(filter_checkbox)
            input_HTML = `<input type="text" id="item-value" value="${value}" class="swal2-input" placeholder="${item}">
                            <input type="checkbox" id="is_filterable" value="${is_filterable_value}" class="filled-in" checked="">
                            <label for="basic_checkbox_2" >Include as a filter option</label>`
        } else {
            input_HTML = `<input type="text" id="item-value"  value="${value}" class="swal2-input" placeholder="${item}">`
        }
        Swal.fire({
            title: 'Update ' + item,
            html: input_HTML,
            iconHtml: '<i class="material-icons" style="color: #3fc3ee; ">edit</i>',
            confirmButtonText: 'Save',
            focusConfirm: false,
            icon: 'info',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            preConfirm: () => {
                const value = Swal.getPopup().querySelector('#item-value').value
                var is_filterable = false
                if (filter_checkbox) {
                    is_filterable = Swal.getPopup().querySelector('#is_filterable').value
                }
                if (!value) {
                    Swal.showValidationMessage(`Please enter a value`)
                }
                return {value: value, is_filterable: is_filterable}
            }
        }).then((result) => {
            var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
            console.log($crf_token)
            $.ajax({
                url: "/api/v1/content/" + item + "-details/" + lkp_id.toString() + '/',
                type: 'put',
                contentType: 'application/json',
                data: `{
                            "title": "${result.value.value.trim()}",
                            "value": "${result.value.value.trim()}",
                            "exclude_from_filter": ${result.value.is_filterable}
                        }`,
                success: function (data) {
                    console.log("success");
                    console.log(data);
                    Swal.fire(
                        'Updated!',
                        `${item} (${value}) has been updated.`,
                        'success'
                    )
                    setTimeout(function () {
                        window.location = redirect_url;
                    }, 1200)
                },
                error: function (data) {
                    Swal.fire(
                        'Failed',
                        `Failed to update ${item} (${value}) !!`,
                        'error'
                    )
                    console.log("error");
                    console.log(data);
                },
                cache: false,
                processData: false,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

        })
    })
}

function delete_item(lckp_id, item, redirect_url) {
    $(function () {
            console.log("click");
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success',
                    cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    //do your own request an handle the results
                    $.ajax({
                        url: "/api/v1/content/" + item + "-details/" + lckp_id.toString() + "/",
                        type: 'delete',
                        data: {
                            'pk': lckp_id,
                        },
                        success: function (data) {
                            console.log("success");
                            console.log(data);
                            swalWithBootstrapButtons.fire(
                                'Deleted!',
                                item + '(' + lckp_id.toString() + ') has been deleted.',
                                'success'
                            )
                            setTimeout(function () {
                                window.location = redirect_url;
                            }, 2000)


                        },
                        error: function (data) {

                            swalWithBootstrapButtons.fire(
                                'Failed',
                                'Failed to delete ' + item + '(' + lckp_id.toString() + ') !!',
                                'error'
                            )
                            console.log("error");
                            console.log(data);
                        },
                        cache: false,
                        contentType: false,
                        processData: false,
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    });

                } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
                ) {
                    // {#swalWithBootstrapButtons.fire(#}
                    // {#    'Cancelled',#}
                    // {#    item + '(' + lckp_id.toString() + ') is safe :)',#}
                    // {#    'error'#}
                    // {#)#}
                }
            })


        }
    )
    ;
}


function delete_user(username) {
    $(function () {
            console.log("click");
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success',
                    cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    //do your own request an handle the results
                    $.ajax({
                        url: "/api/v1/content/user-details/" + username.toString() + "/",
                        type: 'delete',
                        data: {
                            'username': username,
                        },
                        success: function (data) {
                            console.log("success");
                            console.log(data);
                            swalWithBootstrapButtons.fire(
                                'Deleted!',
                                'User' + '(' + username.toString() + ') has been deleted.',
                                'success'
                            )
                            setTimeout(function () {
                                window.location = /user-list/;
                            }, 2000)


                        },
                        error: function (data) {

                            swalWithBootstrapButtons.fire(
                                'Failed',
                                'Failed to delete user (' + username.toString() + ') !!',
                                'error'
                            )
                            console.log("error");
                            console.log(data);
                        },
                        cache: false,
                        contentType: false,
                        processData: false,
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
                    });

                } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
                ) {
                    // {#swalWithBootstrapButtons.fire(#}
                    // {#    'Cancelled',#}
                    // {#    item + '(' + lckp_id.toString() + ') is safe :)',#}
                    // {#    'error'#}
                    // {#)#}
                }
            })


        }
    )
    ;
}

// <script src="https://unpkg.com/@ungap/custom-elements-builtin"></script>
// <script type="module" src="https://unpkg.com/x-frame-bypass.js"></script>