function toggleDropdown() {
    const menu = document.getElementById("dropdown-menu");
    menu.classList.toggle("hidden");
}
document.addEventListener("click", function(e) {
    const avatar = document.querySelector('.avatar-wrapper');
    const dropdown = document.getElementById("dropdown-menu");
    if (avatar && !avatar.contains(e.target)){
        dropdown.classList.add("hidden");
    }
});
