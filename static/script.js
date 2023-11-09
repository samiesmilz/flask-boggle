// Wait for the document to be fully loaded and ready.
// When the document is ready, listen for the submit event on the guess form
$(document).ready(() => {
  $("#guess-form").submit(handleFormSubmission);
  // Start the countdown
  countdownInterval = setInterval(updateTimer, 1000);
  $("#hint-btn").click(getHint);
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
    const coordinates = response.data.coordinates;

    // Check if the guess was correct and get coordinates if available
    if (result === "Congrats - You got it right!" && coordinates?.length) {
      // Add a class to the cells containing the correctly guessed word
      coordinates.forEach((coord) => {
        const [y, x] = coord;
        $(`.row:eq(${y}) .cell:eq(${x})`).addClass("correct-guess");
      });
    }

    $("#score-value").text(points);
    $("#result-message").text(result);
    console.debug("Result displayed.");
    $("#guess-input").val("");
  } catch (error) {
    console.error("Error:", error);
  }
}

let timeRemaining = 60;
let countdownInterval;

// Function to update the timer
function updateTimer() {
  $("#timer").text(timeRemaining);
  if (timeRemaining <= 0) {
    clearInterval(countdownInterval);
    $("#guess-input").prop("disabled", true);
    $("#submit-btn").attr("disabled", true);
    submitScore();
  }
  timeRemaining--;
}

async function submitScore() {
  const score = $("#score-value").text();
  console.log(score);
  try {
    const res = await axios.post("/post-score", { score });
    const highestScore = res.data.score;
    const numOfPlays = res.data.no_of_plays;
    $("#highest-score-span").text(
      highestScore + " - Number of plays : " + numOfPlays
    );
  } catch (error) {
    console.error("Error:", error);
  }
}

async function getHint() {
  console.log("Hint button clicked."); // Add this line
  try {
    const response = await axios.get("/get-hint");
    const hint = response.data.hint;
    const coordinates = response.data.coordinates;

    if (hint === "No more hints available.") {
      // Display a message if no more hints are available
      $("#result-message").text(hint);
    } else if (coordinates.length > 0) {
      // Apply a class to the cells containing the hint
      coordinates.forEach((coord) => {
        const [y, x] = coord;
        $(`.row:eq(${y}) .cell:eq(${x})`).addClass("hinted-cell");
      });

      // Display a hint message
      $("#result-message").text(`Hint: The word starts with "${hint}"`);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
