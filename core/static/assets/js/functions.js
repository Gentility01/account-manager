$(document).ready(function() {
    $("#reviewform").submit(function(e) {
        e.preventDefault();

        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function(response) {
                console.log("comment saved", response);

                if (response.bool === true) {
                    $("#review-comment").html("<h2>Review Added successfully</h2>");
                    $(".hide-comment-form").hide();

                    let context = response.context;
                    let created_at = new Date().toLocaleDateString('en-GB', {
                        day: '2-digit', month: 'short', year: 'numeric'
                    });

                    // Construct a unique ID for the new comment
                    let commentId = `comments-${context.id}`;

                    // Check if the comment already exists
                    if ($(`#${commentId}`).length === 0) {
                        let _html = `
                          <li class="comment-list" id="${commentId}">
                            <div class="comment-avatar text-center">
                              <img src="${staticUrl}" alt="" />
                              <div class="product-rating mt-10">
                                ${generateStarRating(context.rating)}
                              </div>
                            </div>
                            <div class="comment-desc">
                              <span>${created_at}</span>
                              <h4>${context.user.name}</h4>
                              <p>${context.review}</p>
                            </div>
                          </li>`;

                        // Prepend to the correct parent element containing the list of comments
                        $(".comments-container").prepend(_html);
                    } else {
                        console.log("Comment already exists.");
                    }
                } else {
                    console.error("Failed to save comment:", response.errors);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    });

    function generateStarRating(rating) {
        let fullStars = Math.floor(rating);
        let emptyStars = 5 - fullStars;

        let starHtml = '';

        for (let i = 0; i < fullStars; i++) {
            starHtml += '<i class="fa fa-star"></i>'; // Full star
        }

        for (let i = 0; i < emptyStars; i++) {
            starHtml += '<i class="fa fa-star-o"></i>'; // Empty star
        }

        return starHtml;
    }
});



// --------------------------------------fiilter product
$(document).ready(function() {
    // Event handler for clicking on filter checkboxes or the price filter button
    $(".filter-checkbox, #price-filter-btn").on("click", function() {
        console.log("Checkbox or button clicked");

        // Initialize an empty object to hold the filter criteria
        let filter_object = {};

        // Get the minimum price from the min attribute of the price input element
        let min_price = $("#max_price").attr("min");
        // Get the current value of the price input element
        let max_price = $("#max_price").val();

        // Add price filters to the filter object only if they are set
        if (min_price) {
            filter_object.min_price = min_price;
        }
        if (max_price) {
            filter_object.max_price = max_price;
        }

        // Iterate over each filter checkbox
        $(".filter-checkbox").each(function() {
            // Get the filter key from the data-filter attribute
            let filter_key = $(this).data("filter");
            // Create an array of checked values for the current filter key
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function(element) {
                return element.value;
            });
        });

        console.log("Filter object is ", filter_object);

        // Send an AJAX request to the server with the filter criteria
        $.ajax({
            url: "/filter-product", // URL to send the request to
            data: filter_object, // Data to be sent to the server
            dataType: "json", // Expect a JSON response from the server
            beforeSend: function() {
                console.log("Before send");
            },
            // Function to handle a successful response
            success: function(response) {
                console.log("Success");
                console.log(response);
                // Update the HTML content of the element with id 'filtered-product' with the response data
                $("#filtered-product").html(response.data);
            },
            // Function to handle errors
            error: function(xhr, status, error) {
                console.log("Error: ", error);
            }
        });
    });

    // Event handler for when the price input loses focus
    $("#max_price").on("blur", function() {
        let min_price = $(this).attr("min"); // Get the minimum price value
        let max_price = $(this).attr("max"); // Get the maximum price value
        let current_price = $(this).val(); // Get the current price value

        console.log(min_price, max_price, current_price);
        // Check if the current price is outside the allowed range
        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            console.log("Error occurred");

            // Round the minimum and maximum prices to two decimal places
            min_price = Math.round(min_price * 100) / 100;
            max_price = Math.round(max_price * 100) / 100;

            // Alert the user about the allowed price range
            alert("Price must be between $" + min_price + " and $" + max_price);
            // Reset the price input value to the minimum price
            $(this).val(min_price);
            // Reset the range input value to the minimum price
            $("#range").val(min_price);
            // Refocus the price input
            $(this).focus();

            return false; // Prevent further execution
        }
    });
});
