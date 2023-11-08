// Wait for the document to be fully loaded and ready.
// When the document is ready, listen for the submit event on the guess form
$(document).ready(() => {
  $("#guess-form").submit(handleFormSubmission);
});

async function handleFormSubmission(event) {
  event.preventDefault();

  // Get the user's guess from the input field.
  const guess = $("#guess-input").val();

  try {
    // Send an AJAX request to the server with the user's guess and await the response.
    const response = await axios.post("/check-guess", { guess });
    console.debug("Request sent...");

    // Handle the server's response and display it directly to the user.
    const result = response.data.result;
    const points = response.data.points;

    $("#score-value").text(points);
    $("#result-message").text(result);
    console.debug("Result displayed.");
  } catch (error) {
    console.error("Error:", error);
  }
}
