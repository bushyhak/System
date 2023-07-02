const toggleButton = document.getElementById("btnToggle");

if (toggleButton) {
	const divNavbarLinks = document.querySelector(".navbar-links");

	toggleButton.addEventListener("click", () => {
		divNavbarLinks.classList.toggle("active");
	});
}
