document.addEventListener("DOMContentLoaded", function () {
  const menuIcon = document.querySelector(".menu-icon");
  const nav = document.querySelector("nav");

  menuIcon.addEventListener("click", function () {
    nav.style.display = nav.style.display === "none" ? "block" : "none";
  });
});
