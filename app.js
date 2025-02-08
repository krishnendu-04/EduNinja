// Reference DOM elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('resultsContainer');

// List of Programming Language YouTube Course URLs (including Python, JavaScript, Java, C++, Ruby, and R)
const languageCourses = [
  // Python Courses
  {
    title: 'Python for Beginners by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=rfscVS0vtbw',
    language: 'Python'
  },
  {
    title: 'Python Tutorial for Beginners by Programming with Mosh',
    url: 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
    language: 'Python'
  },
  {
    title: 'Python for Data Science by Simplilearn',
    url: 'https://www.youtube.com/watch?v=LHBE6Q9XlzI',
    language: 'Python'
  },
  {
    title: 'Python Full Course by Edureka',
    url: 'https://www.youtube.com/watch?v=J8vZJl6NJxo',
    language: 'Python'
  },
  
  // JavaScript Courses
  {
    title: 'JavaScript Crash Course by Traversy Media',
    url: 'https://www.youtube.com/watch?v=hdI2bqOjy3c',
    language: 'JavaScript'
  },
  {
    title: 'JavaScript Tutorial for Beginners by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=PkZNo7MFNFg',
    language: 'JavaScript'
  },
  
  // Java Courses
  {
    title: 'Java Full Course by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=grEKMHGYyns',
    language: 'Java'
  },
  {
    title: 'Java Programming Tutorial for Beginners by Programming with Mosh',
    url: 'https://www.youtube.com/watch?v=eIrMbAQSU34',
    language: 'Java'
  },
  
  // C++ Courses
  {
    title: 'C++ Full Course by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
    language: 'C++'
  },
  {
    title: 'Learn C++ in One Video by CodeWithHarry',
    url: 'https://www.youtube.com/watch?v=8jLOx1hD3O0',
    language: 'C++'
  },
  
  // Ruby Courses
  {
    title: 'Ruby Programming Tutorial by ProgrammingKnowledge',
    url: 'https://www.youtube.com/watch?v=t_isvp25f6c',
    language: 'Ruby'
  },
  {
    title: 'Ruby Full Course by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=t_isvp25f6c',
    language: 'Ruby'
  },
  
  // R Programming Courses
  {
    title: 'R Programming Tutorial for Beginners by Programming with Mosh',
    url: 'https://www.youtube.com/watch?v=_V8eKsto3Ug',
    language: 'R'
  },
  {
    title: 'R Programming Full Course by freeCodeCamp',
    url: 'https://www.youtube.com/watch?v=fDrdQfmHbks',
    language: 'R'
  },
  {
    title: 'Learn R Programming in One Video by CodeWithHarry',
    url: 'https://www.youtube.com/watch?v=0JfKMg0aXWI',
    language: 'R'
  },
  {
    title: 'R Programming for Data Science by Simplilearn',
    url: 'https://www.youtube.com/watch?v=8B2p53Efhv8',
    language: 'R'
  }
];

// Add event listener for the search button
searchBtn.addEventListener('click', async () => {
  const query = searchInput.value.trim();

  // Check if input is not empty
  if (query) {
    // Filter the courses based on the search query
    const filteredCourses = languageCourses.filter(course => 
      course.title.toLowerCase().includes(query.toLowerCase()) ||
      course.language.toLowerCase().includes(query.toLowerCase())
    );
    
    // Display filtered results
    displayResults(filteredCourses);
  } else {
    alert('Please enter a search term.');
  }
});

// Function to display the course results
function displayResults(courses) {
  // Clear any previous results
  resultsContainer.innerHTML = '';

  // If no courses found, show a message
  if (courses.length === 0) {
    resultsContainer.innerHTML = '<p>No courses found for this search.</p>';
    return;
  }

  // Create a card for each course
  courses.forEach(course => {
    const courseCard = document.createElement('div');
    courseCard.classList.add('course-card');

    // Add course title, language, and link
    courseCard.innerHTML = `
      <h3><a href="${course.url}" target="_blank">${course.title}</a></h3>
      <p><strong>Language:</strong> ${course.language}</p>
      <a href="${course.url}" target="_blank">View Course</a>
    `;

    // Append the course card to the results container
    resultsContainer.appendChild(courseCard);
  });
}



document.getElementById('signupForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form from submitting normally

  // Get form values
  const fullName = document.getElementById('fullName').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  // Basic form validation
  if (!fullName || !email || !password || !confirmPassword) {
      alert("All fields are required.");
      return;
  }

  if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
  }

  // Sending the data to the server (you would need to set up server-side to handle this POST request)
  const userData = {
      fullName,
      email,
      password
  };

  fetch('/submit_signup', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert('Account created successfully!');
          window.location.href = 'login.html'; // Redirect to login page
      } else {
          alert('Error: ' + data.message);
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Something went wrong!');
  });
});
