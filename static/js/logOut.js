var logOutButton = document.getElementById('logoutButton');

logOutButton.addEventListener('click', () => {
    Swal.fire({
        title: "Logging out",
        text: "Are you sure you want to log out?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, log out",
        cancelButtonText: "Cancel"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/logOut';
        }
    })
})