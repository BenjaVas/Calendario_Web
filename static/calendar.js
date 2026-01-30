

let currentDate = new Date();

function renderCalendars() {
    renderCalendar("calendar1", currentDate);

    let nextMonth = new Date(currentDate);
    nextMonth.setMonth(nextMonth.getMonth() + 1);
    renderCalendar("calendar2", nextMonth);

    const title = document.getElementById("calendar-title");
    if (title) {
        title.innerText = currentDate.toLocaleDateString("es-ES", {
            month: "long",
            year: "numeric"
        });
    }
}

function renderCalendar(containerId, date) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "";

    const month = date.getMonth();
    const year = date.getFullYear();

    const title = document.createElement("h3");
    title.innerText = date.toLocaleDateString("es-ES", {
        month: "long",
        year: "numeric"
    });
    container.appendChild(title);

    const days = document.createElement("div");
    days.className = "days";

    const firstDay = new Date(year, month, 1).getDay();
    const totalDays = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        days.appendChild(document.createElement("div"));
    }

    for (let d = 1; d <= totalDays; d++) {
        const cell = document.createElement("div");
        cell.className = "day";
        cell.innerText = d;

        const cellDate = new Date(year, month, d);

        if (typeof proyectos !== "undefined") {
            proyectos.forEach(p => {
                const start = new Date(p.inicio);
                const end = new Date(p.fin);

                if (!isNaN(start) && !isNaN(end)) {
                    if (cellDate >= start && cellDate <= end) {
                        cell.classList.add("project");
                        cell.style.background = p.color;
                    }
                }
            });
        }

        days.appendChild(cell);
    }

    container.appendChild(days);
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendars();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendars();
}

renderCalendars();