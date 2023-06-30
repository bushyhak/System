const toggleButton = document.getElementById('btnToggle');

const divNavbarLinks = document.querySelector('.navbar-links');

toggleButton.addEventListener('click', () => {
    divNavbarLinks.classList.toggle('active');
})
