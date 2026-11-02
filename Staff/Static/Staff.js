
/* =====================================
   SMARTATTEND - STAFF JAVASCRIPT
===================================== */

// SIDEBAR TOGGLE

const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");

if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("show");
    });
}

// CLOSE SIDEBAR ON MOBILE

document.querySelectorAll(".sidebar-menu .menu-link").forEach(link => {
    link.addEventListener("click", () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove("show");
        }
    });
});


// ACTIVE SIDEBAR MENU

const menuLinks = document.querySelectorAll(".menu-link");

menuLinks.forEach(link => {
    link.addEventListener("click", () => {
        menuLinks.forEach(item => item.classList.remove("active"));
        link.classList.add("active");
    });
});


// STUDENT SEARCH

const searchInput = document.getElementById("studentSearch");
const attendanceFilter = document.getElementById("attendanceFilter");

function filterStudents() {

    const searchValue = searchInput
        ? searchInput.value.toLowerCase().trim()
        : "";

    const filterValue = attendanceFilter
        ? attendanceFilter.value.toLowerCase()
        : "";

    const rows = document.querySelectorAll(
        "#studentTable tbody tr"
    );

    rows.forEach(row => {

        if (row.cells.length < 6) return;

        const studentName =
            row.cells[0].textContent.toLowerCase();

        const studentId =
            row.cells[1].textContent.toLowerCase();

        const attendanceStatus =
            row.cells[3].textContent.toLowerCase().trim();

        const matchesSearch =
            studentName.includes(searchValue) ||
            studentId.includes(searchValue);

        const matchesAttendance =
            !filterValue ||
            attendanceStatus.includes(filterValue);

        row.style.display =
            matchesSearch && matchesAttendance ? "" : "none";

    });
}

if (searchInput) {
    searchInput.addEventListener("input", filterStudents);
}

if (attendanceFilter) {
    attendanceFilter.addEventListener(
        "change",
        filterStudents
    );
}


// ADD STUDENT BUTTON

const addStudentBtn =
    document.getElementById("addStudentBtn");

if (addStudentBtn) {
    addStudentBtn.addEventListener("click", () => {
        window.location.href = "/staff/students/add/";
    });
}


// EDIT STUDENT BUTTON

document.addEventListener("click", function(event) {

    const editButton = event.target.closest(".edit-btn");

    if (!editButton) return;

    const studentId = editButton.dataset.id;

    if (!studentId) return;

    window.location.href =
        "/staff/students/edit/" +
        encodeURIComponent(studentId) + "/";

});


// DELETE STUDENT BUTTON

document.addEventListener("click", function(event) {

    const deleteButton = event.target.closest(".delete-btn");

    if (!deleteButton) return;

    const studentId = deleteButton.dataset.id;

    if (!studentId) return;

    const confirmed = confirm(
        "Are you sure you want to delete this student?"
    );

    if (confirmed) {

        const form = document.createElement("form");

        form.method = "POST";
        form.action =
            "/staff/students/delete/" +
            encodeURIComponent(studentId) + "/";

        const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );

        if (!csrfToken) {
            alert("Security token missing. Please refresh the page.");
            return;
        }

        const csrfInput = document.createElement("input");

        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = csrfToken.value;

        form.appendChild(csrfInput);

        document.body.appendChild(form);

        form.submit();
    }

});


// NOTIFICATION BUTTON

const notificationBtn =
    document.querySelector(".notification-btn");

if (notificationBtn) {

    notificationBtn.addEventListener("click", () => {

        alert("Your notifications will appear here.");

    });

}


// PROFILE EDIT BUTTON

document.querySelectorAll(
    ".outline-btn"
).forEach(button => {

    if (button.textContent.includes("Edit Profile")) {

        button.addEventListener("click", () => {

            window.location.href =
                "/staff/profile/edit/";

        });

    }

});


// LOGOUT CONFIRMATION

const logoutLink =
    document.querySelector(".logout-link");

if (logoutLink) {

    logoutLink.addEventListener("click", function(event) {

        const confirmed = confirm(
            "Are you sure you want to logout?"
        );

        if (!confirmed) {
            event.preventDefault();
        }

    });

}


// SMOOTH SECTION NAVIGATION

document.querySelectorAll(
    '.sidebar-menu a[href^="#"]'
).forEach(link => {

    link.addEventListener("click", function(event) {

        const target = document.querySelector(
            this.getAttribute("href")
        );

        if (target) {

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

            history.replaceState(
                null,
                "",
                this.getAttribute("href")
            );

        }

    });

});


// RESPONSIVE SIDEBAR

window.addEventListener("resize", () => {

    if (window.innerWidth > 768 && sidebar) {
        sidebar.classList.remove("show");
    }

});


// PAGE INITIALIZATION

document.addEventListener("DOMContentLoaded", () => {

    console.log("SmartAttend Staff Portal Initialized");

});
