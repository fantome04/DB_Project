const BASE_URL = "http://127.0.0.1:8000";

let driverPage = 1;
let circuitPage = 1;
let racePage = 1;
const pageSize = 10;

function showMessage(container, message, type) {
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

async function fetchData(endpoint, targetElement, renderCallback, skip = 0, limit = pageSize, callbackIfEmpty = null) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}?skip=${skip}&limit=${limit}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Unknown error");
        }
        const data = await response.json();
        if (data.length === 0 && callbackIfEmpty) {
            callbackIfEmpty();
        } else {
            renderCallback(data, targetElement, data.length);
        }

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function createListItem(item, onDelete, onUpdate) {
    const listItem = document.createElement("div");
    listItem.className = "list-group-item";

    const content = document.createElement("pre");
    content.textContent = JSON.stringify(item, null, 2);

    const deleteButton = document.createElement("button");
    deleteButton.className = "btn btn-danger btn-sm m-1";
    deleteButton.textContent = "Delete";
    deleteButton.onclick = () => onDelete(item);

    const updateButton = document.createElement("button");
    updateButton.className = "btn btn-secondary btn-sm m-1";
    updateButton.textContent = "Update";
    updateButton.onclick = () => onUpdate(item);

    listItem.append(content, deleteButton, updateButton);
    return listItem;
}

function renderList(data, targetElement, onDelete, onUpdate, paginationContainer, loadPageCallback, currentPage) {
    targetElement.innerHTML = "";

    if (data.length === 0) {
        targetElement.innerHTML = "<p class='text-center'>No data found.</p>";
        paginationContainer.innerHTML = "";
        return;
    }

    data.forEach(item => {
        const listItem = createListItem(item, onDelete, onUpdate);
        targetElement.appendChild(listItem);
    });

    renderPagination(paginationContainer, currentPage, loadPageCallback, data.length);
}

function renderPagination(container, currentPage, loadPageCallback, dataLength) {
    container.innerHTML = `
        <button class="btn btn-primary btn-sm me-2" ${currentPage <= 1 ? "disabled" : ""}>
            Previous
        </button>
        <span class="mx-2">Page ${currentPage}</span>
        <button class="btn btn-primary btn-sm ms-2" ${dataLength < pageSize ? "disabled" : ""}>
            Next
        </button>
    `;

    const buttons = container.querySelectorAll("button");
    buttons[0]?.addEventListener("click", () => loadPageCallback(currentPage - 1));
    buttons[1]?.addEventListener("click", () => loadPageCallback(currentPage + 1));
}

document.getElementById("driver-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const driverMessage = document.getElementById("driver-message");
    const driverData = {
        id: parseInt(document.getElementById("driver-id").value),
        number: parseInt(document.getElementById("driver-number").value),
        name: document.getElementById("driver-name").value,
        nationality: document.getElementById("driver-nationality").value,
        team: document.getElementById("driver-team").value,
        dob: document.getElementById("driver-dob").value,
        details: JSON.parse(document.getElementById("driver-details").value),
    };
    try {
        const response = await fetch(`${BASE_URL}/drivers/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(driverData),
        });
        if (response.ok) {
            showMessage(driverMessage, "Driver added successfully!", "success");
            loadDrivers(driverPage);
            document.getElementById("driver-form").reset();
        } else {
            const errorData = await response.json();
            showMessage(driverMessage, `Error adding driver: ${errorData.detail || "Unknown error"}`, "danger");
        }
    } catch (error) {
        console.error("Error:", error);
        showMessage(driverMessage, `Error adding driver: ${error.message}`, "danger");
    }
});

async function loadDrivers(page = 1) {
    driverPage = page;
    const skip = (driverPage - 1) * pageSize;
    
    fetchData(
        "/drivers",
        document.getElementById("drivers-list"),
        (data, target) => renderList(
            data,
            target,
            deleteDriver,
            updateDriver,
            document.getElementById("driver-pagination"),
            loadDrivers,
            driverPage
        ),
        skip
    );
}

async function deleteDriver(driver) {
    const driverMessage = document.getElementById("driver-message");
    if (confirm(`Are you sure you want to delete driver ${driver.name}?`)) {
        try {
            const response = await fetch(`${BASE_URL}/drivers/${driver.id}`, { method: "DELETE" });
            if (response.ok) {
                showMessage(driverMessage, "Driver deleted successfully!", "success");
                loadDrivers(driverPage);
            } else {
                const errorData = await response.json();
                showMessage(driverMessage, `Error deleting driver: ${errorData.detail || "Unknown error"}`, "danger");
            }
        } catch (error) {
            console.error("Error:", error);
            showMessage(driverMessage, `Error deleting driver: ${error.message}`, "danger");
        }
    }
}

function updateDriver(driver) {
    const driverMessage = document.getElementById("driver-message");
    const updatedName = prompt("Enter new name:", driver.name);
    if (updatedName) {
        const updatedData = { ...driver, name: updatedName };
        fetch(`${BASE_URL}/drivers/${driver.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedData),
        })
            .then(async response => {
                if (response.ok) {
                    showMessage(driverMessage, "Driver updated successfully!", "success");
                    loadDrivers(driverPage);
                } else {
                    const errorData = await response.json();
                    showMessage(driverMessage, `Error updating driver: ${errorData.detail || "Unknown error"}`, "danger");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showMessage(driverMessage, `Error updating driver: ${error.message}`, "danger");
            });
    }
}

document.getElementById("circuit-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const circuitMessage = document.getElementById("circuit-message");
    const circuitData = {
        id: parseInt(document.getElementById("circuit-id").value),
        name: document.getElementById("circuit-name").value,
        location: document.getElementById("circuit-location").value,
        length: parseFloat(document.getElementById("circuit-length").value),
        laps: parseInt(document.getElementById("circuit-laps").value),
        lap_record: document.getElementById("circuit-lap-record").value,
    };
    try {
        const response = await fetch(`${BASE_URL}/circuits/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(circuitData),
        });
        if (response.ok) {
            showMessage(circuitMessage, "Circuit added successfully!", "success");
            loadCircuits(circuitPage);
            document.getElementById("circuit-form").reset();
        } else {
            const errorData = await response.json();
            showMessage(circuitMessage, `Error adding circuit: ${errorData.detail || "Unknown error"}`, "danger");
        }
    } catch (error) {
        console.error("Error:", error);
        showMessage(circuitMessage, `Error adding circuit: ${error.message}`, "danger");
    }
});

async function loadCircuits(page = 1) {
    circuitPage = page;
    const skip = (circuitPage - 1) * pageSize;
    fetchData(
        "/circuits",
        document.getElementById("circuits-list"),
        (data, target) => renderList(
            data,
            target,
            deleteCircuit,
            updateCircuit,
            document.getElementById("circuit-pagination"),
            loadCircuits,
            circuitPage
        ),
        skip
    );
}

async function deleteCircuit(circuit) {
    const circuitMessage = document.getElementById("circuit-message");
    if (confirm(`Are you sure you want to delete circuit ${circuit.name}?`)) {
        try {
            const response = await fetch(`${BASE_URL}/circuits/${circuit.id}`, { method: "DELETE" });
            if (response.ok) {
                showMessage(circuitMessage, "Circuit deleted successfully!", "success");
                loadCircuits(circuitPage);
            } else {
                const errorData = await response.json();
                showMessage(circuitMessage, `Error deleting circuit: ${errorData.detail || "Unknown error"}`, "danger");
            }
        } catch (error) {
            console.error("Error:", error);
            showMessage(circuitMessage, `Error deleting circuit: ${error.message}`, "danger");
        }
    }
}

function updateCircuit(circuit) {
    const circuitMessage = document.getElementById("circuit-message");
    const updatedName = prompt("Enter new circuit name:", circuit.name);
    if (updatedName) {
        const updatedData = { ...circuit, name: updatedName };
        fetch(`${BASE_URL}/circuits/${circuit.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedData),
        })
            .then(async response => {
                if (response.ok) {
                    showMessage(circuitMessage, "Circuit updated successfully!", "success");
                    loadCircuits(circuitPage);
                } else {
                    const errorData = await response.json();
                    showMessage(circuitMessage, `Error updating circuit: ${errorData.detail || "Unknown error"}`, "danger");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showMessage(circuitMessage, `Error updating circuit: ${error.message}`, "danger");
            });
    }
}

document.getElementById("race-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const raceMessage = document.getElementById("race-message");
    const raceData = {
        driver_id: parseInt(document.getElementById("race-driver-id").value),
        circuit_id: parseInt(document.getElementById("race-circuit-id").value),
        race_date: document.getElementById("race-date").value,
        place: parseInt(document.getElementById("race-place").value),
        points: parseInt(document.getElementById("race-points").value),
        is_fastest_lap: document.getElementById("race-fastest-lap").checked,
        start_place: parseInt(document.getElementById("race-start-place").value),
    };
    try {
        const response = await fetch(`${BASE_URL}/races/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(raceData),
        });
        if (response.ok) {
            showMessage(raceMessage, "Race added successfully!", "success");
            loadRaces(racePage);
            document.getElementById("race-form").reset();
        } else {
            const errorData = await response.json();
            showMessage(raceMessage, `Error adding race: ${errorData.detail || "Unknown error"}`, "danger");
        }
    } catch (error) {
        console.error("Error:", error);
        showMessage(raceMessage, `Error adding race: ${error.message}`, "danger");
    }
});

async function loadRaces(page = 1) {
    racePage = page;
    const skip = (racePage - 1) * pageSize;
    fetchData(
        "/races",
        document.getElementById("races-list"),
        (data, target) => renderList(
            data,
            target,
            deleteRace,
            updateRace,
            document.getElementById("race-pagination"),
            loadRaces,
            racePage
        ),
        skip
    );
}

async function deleteRace(race) {
    const raceMessage = document.getElementById("race-message");
    if (confirm(`Are you sure you want to delete race on ${race.race_date}?`)) {
        try {
            const response = await fetch(`${BASE_URL}/races/${race.driver_id}/${race.circuit_id}/${race.race_date}`, {
                method: "DELETE"
            });
            if (response.ok) {
                showMessage(raceMessage, "Race deleted successfully!", "success");
                loadRaces(racePage);
            } else {
                const errorData = await response.json();
                showMessage(raceMessage, `Error deleting race: ${errorData.detail || "Unknown error"}`, "danger");
            }
        } catch (error) {
            console.error("Error:", error);
            showMessage(raceMessage, `Error deleting race: ${error.message}`, "danger");
        }
    }
}

function updateRace(race) {
    const raceMessage = document.getElementById("race-message");
    const updatedPoints = prompt("Enter new points:", race.points);
    if (updatedPoints) {
        const updatedData = { ...race, points: parseInt(updatedPoints) };
        fetch(`${BASE_URL}/races/${race.driver_id}/${race.circuit_id}/${race.race_date}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedData),
        })
            .then(async response => {
                if (response.ok) {
                    showMessage(raceMessage, "Race updated successfully!", "success");
                    loadRaces(racePage);
                } else {
                    const errorData = await response.json();
                    showMessage(raceMessage, `Error updating race: ${errorData.detail || "Unknown error"}`, "danger");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showMessage(raceMessage, `Error updating race: ${error.message}`, "danger");
            });
    }
}

loadDrivers();
loadCircuits();
loadRaces();
