// Reference DOM elements
const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');

// Add event listener for the login form
loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();  // Prevent the page from refreshing when submitting

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  // Simple validation
  if (!email || !password) {
    alert('Please fill in both fields');
    return;
  }

  // Example: Fake backend authentication for demonstration purposes
  // Replace this with actual authentication logic (e.g., API call to the backend)
  const fakeUsers = [
    { email: 'user1@example.com', password: 'password123' },
    { email: 'user2@example.com', password: 'password456' }
  ];

  const user = fakeUsers.find(user => user.email === email && user.password === password);

  if (user) {
    alert('Login successful!');
    // Redirect to a different page (e.g., dashboard, home page, etc.)
    window.location.href = 'dashboard.html';  // Redirect example
  } else {
    alert('Invalid credentials. Please try again.');
  }
});

