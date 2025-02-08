document.addEventListener("DOMContentLoaded", () => {
  const messagesElement = document.querySelector(".messages");

  if (messagesElement) {
    setTimeout(() => {
      messagesElement.style.display = "none";
    }, 3000);
  }
});
document.addEventListener("DOMContentLoaded", function () {
  const navItems = document.querySelector(".nav_item");
  const openNavBtn = document.querySelector("#open_nav-btn");
  const closeNavBtn = document.querySelector("#close_nav-btn");

  // Open nav dropdown
  const openNav = () => {
    navItems.style.display = "flex";
    openNavBtn.style.display = "none";
    closeNavBtn.style.display = "inline-block";
  };

  // Close nav dropdown
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

  // Show sidebar on small devices
  const showSidebar = () => {
    sidebar.style.left = "0";
    showSidebarbtn.style.display = "none";
    hideSidebarbtn.style.display = "inline-block";
  };

  // Hide sidebar on small devices
  const hideSidebar = () => {
    sidebar.style.left = "-100%";
    showSidebarbtn.style.display = "inline-block";
    hideSidebarbtn.style.display = "none";
  };

  showSidebarbtn?.addEventListener("click", showSidebar);
  hideSidebarbtn?.addEventListener("click", hideSidebar);

  // Language dropdown
  const dropdown = document.querySelector(".custom-dropdown");
  const selected = document.querySelector(".custom-selected");
  const options = document.querySelector(".custom-options");
  const hiddenSelect = document.getElementById("language-dropdown");

  if (dropdown && selected && options && hiddenSelect) {
    // Toggle dropdown visibility
    selected.addEventListener("click", (e) => {
      dropdown.classList.toggle("active");
      options.style.display = dropdown.classList.contains("active")
        ? "block"
        : "none";
      e.stopPropagation();
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target) && !selected.contains(e.target)) {
        dropdown.classList.remove("active");
        options.style.display = "none";
      }
    });

    // Handle selection
    options.addEventListener("click", (e) => {
      const option = e.target.closest("li");
      if (option) {
        const value = option.getAttribute("data-value");
        const flag = option.getAttribute("data-flag");
        const text = option.textContent.trim();

        selected.querySelector("span").textContent = text;
        selected.querySelector("img").src = flag;
        hiddenSelect.value = value;

        dropdown.classList.remove("active");
        options.style.display = "none";
      }
    });
  }

  // Dropdown
  const settingsIcon = document.querySelector(".settings_icon");
  const settingsDropdown = document.querySelector(".nav_profile ul");

  if (settingsIcon && settingsDropdown) {
    // Toggle dropdown visibility when clicking the settings icon
    settingsIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      settingsDropdown.classList.toggle("active");
      settingsDropdown.style.display = settingsDropdown.classList.contains(
        "active"
      )
        ? "block"
        : "none";
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
      if (
        !settingsIcon.contains(e.target) &&
        !settingsDropdown.contains(e.target)
      ) {
        settingsDropdown.classList.remove("active");
        settingsDropdown.style.display = "none";
      }
    });
  }
});
