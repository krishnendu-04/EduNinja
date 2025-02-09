document.getElementById("searchBtn").addEventListener("click", async () => {
  const query = document.getElementById("searchInput").value.trim();
  const response = await fetch(`/search?query=${query}`);
  const data = await response.json();

  const resultsContainer = document.getElementById("resultsContainer");
  resultsContainer.innerHTML = "";
  
  if (data.courses) {
    data.courses.forEach(course => {
      const div = document.createElement("div");
      div.innerHTML = `<h3>${course.title}</h3><p><a href="${course.url}" target="_blank">View Course</a></p>`;
      resultsContainer.appendChild(div);
    });
  } else {
    resultsContainer.innerHTML = "<p>No courses found.</p>";
  }
});
