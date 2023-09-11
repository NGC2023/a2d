// Function to perform the logout and redirect to the logout page.
function logoutUser() {
  localStorage.clear(); // You can use sessionStorage instead for a session-specific logout.
  window.location.href = '/logout'; // Replace '/logout' with the URL for your logout page or endpoint.
}

// Interval in milliseconds for the inactivity period (e.g., 30 minutes).
const INACTIVITY_PERIOD = 20 * 60 * 1000;

// Function to reset the inactivity timer.
function resetInactivityTimer() {
  clearTimeout(window.inactivityTimer);
  window.inactivityTimer = setTimeout(logoutUser, INACTIVITY_PERIOD);
}

// Start the inactivity timer when the page loads.
document.addEventListener('DOMContentLoaded', function () {
  resetInactivityTimer();

  // Reset the timer when any user interaction occurs (e.g., click, keypress).
  window.addEventListener('click', resetInactivityTimer);
  window.addEventListener('keydown', resetInactivityTimer);
});
