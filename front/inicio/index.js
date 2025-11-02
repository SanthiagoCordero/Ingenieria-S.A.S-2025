// Menú hamburguesa
const menuToggle = document.getElementById("menu-toggle");
const navMenu = document.querySelector("nav ul");
const dropdown = document.querySelector(".dropdown");

menuToggle.addEventListener("click", () => {
  navMenu.classList.toggle("active");
});

// Submenú desplegable en móvil
dropdown.addEventListener("click", (e) => {
  e.stopPropagation();
  dropdown.classList.toggle("active");
});

// Header: transparente al inicio y sólido al hacer scroll
const header = document.querySelector("header");
const updateHeaderOnScroll = () => {
  if (window.scrollY > 10) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
};


// Cambia el estado del header según visibilidad del hero
const hero = document.querySelector(".hero");
if ("IntersectionObserver" in window && hero) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          header.classList.remove("scrolled");
        } else {
          header.classList.add("scrolled");
        }
      });
    },
    { threshold: 0.1 }
  );
  observer.observe(hero);
} else {
  // Fallback basado en scroll
  const updateHeaderOnScrollFallback = () => {
    if (window.scrollY > 10) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  };
  updateHeaderOnScrollFallback();
  window.addEventListener("scroll", updateHeaderOnScrollFallback);
}
