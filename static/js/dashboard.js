// ------- Sidebar Toggle (Mobile) -------
function toggleSidebar() {
    let sb = document.getElementById("sidebar");
    sb.classList.toggle("active");
}

// ------- Search Filter -------
let searchBox = document.getElementById("search");
if (searchBox) {
    searchBox.addEventListener("keyup", function () {
        let value = searchBox.value.toLowerCase();
        let rows = document.querySelectorAll("#patientTable tr");

        rows.forEach(row => {
            let name = row.children[1].textContent.toLowerCase();
            if (name.includes(value)) row.style.display = "";
            else row.style.display = "none";
        });
    });
}

// ------- Counter Animation -------
function animateCounter(id, target) {
    let c = document.getElementById(id);
    let count = 0;
    let speed = target / 80;

    let update = setInterval(() => {
        count += speed;
        if (count >= target) {
            c.innerText = target;
            clearInterval(update);
        } else {
            c.innerText = Math.floor(count);
        }
    }, 20);
}

// Call animations
animateCounter("count1", 120);
animateCounter("count2", 85);
animateCounter("count3", 32);
animateCounter("count4", 14);
