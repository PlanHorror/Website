const navItems = document.querySelector(".nav_item");
const openNavBtn = document.querySelector("#open_nav-btn");
const closeNavBtn = document.querySelector("#close_nav-btn");

// open nav dropdown
const openNav = () => {
  navItems.style.display = "flex";
  openNavBtn.style.display = "none";
  closeNavBtn.style.display = "inline-block";
};

// close nav dropdown
const closeNav = () => {
  navItems.style.display = "none";
  openNavBtn.style.display = "inline-block";
  closeNavBtn.style.display = "none";
};

openNavBtn.addEventListener("click", openNav);
closeNavBtn.addEventListener("click", closeNav);

const sidebar = document.querySelector("aside");
const showSidebarbtn = document.querySelector("#show_sidebar-btn");
const hideSidebarbtn = document.querySelector("#hide_sidebar-btn");

// show sidebar on small devices
const showSidebar = () => {
  sidebar.style.left = "0";
  showSidebarbtn.style.display = "none";
  hideSidebarbtn.style.display = "inline-block";
};

// hide sidebar on small devices
const hideSidebar = () => {
  sidebar.style.left = "-100%";
  showSidebarbtn.style.display = "inline-block";
  hideSidebarbtn.style.display = "none";
};

showSidebarbtn.addEventListener("click", showSidebar);
hideSidebarbtn.addEventListener("click", hideSidebar);

// new
const settingsDropdown = document.querySelector(".nav_profile ul li a");
const languageOptions = document.querySelector(".language_options");

settingsDropdown.addEventListener("click", () => {
  if (languageOptions.style.display === "block") {
    languageOptions.style.display = "none";
  } else {
    languageOptions.style.display = "block";
  }
});

//

// Sorting Posts
function sortPosts() {
  const sortSelect = document.getElementById("sort-select");
  const sortBy = sortSelect.value;
  console.log(sortBy);
  // Take loader by class
  const loader = document.querySelector(".loader");
  // Show the loader in full screen
  loader.style.display = "flex";

  // Redirect to the sorted page
  window.location.href = `?sort=${sortBy}`;
}

function filterByTopic() {
  const topicSelect = document.getElementById("topic-menu");
  const topic = topicSelect.value;
  console.log(topic);
  // Take loader by class
  const loader = document.querySelector(".loader");
  // Show the loader in full screen
  loader.style.display = "flex";

  // Redirect to the sorted page
  window.location.href = `?label=${topic}`;
}
function searchPosts() {
  const searchInput = document.getElementById("search");
  const searchValue = searchInput.value;
  console.log(searchValue);
  // Take loader by class
  const loader = document.querySelector(".loader");
  // Show the loader in full screen
  loader.style.display = "flex";

  // Redirect to the sorted page
  window.location.href = `?search=${searchValue}`;
}
