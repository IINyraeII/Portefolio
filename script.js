let applications = JSON.parse(localStorage.getItem("applications")) || [];

const form = document.getElementById("applicationForm");
const applicationList = document.getElementById("applicationList");

form.addEventListener("submit", function(event) {
  event.preventDefault();

  const application = {
    company: document.getElementById("company").value,
    position: document.getElementById("position").value,
    city: document.getElementById("city").value,
    link: document.getElementById("link").value,
    status: document.getElementById("status").value
  };

  applications.push(application);
  saveApplications();
  displayApplications();
  updateDashboard();

  form.reset();
});

function saveApplications() {
  localStorage.setItem("applications", JSON.stringify(applications));
}

function displayApplications() {
  applicationList.innerHTML = "";

  applications.forEach(function(application, index) {
    const div = document.createElement("div");
    div.className = "application-item";

    div.innerHTML = `
      <h3>${application.company}</h3>
      <p><strong>Poste :</strong> ${application.position}</p>
      <p><strong>Ville :</strong> ${application.city}</p>
      <p><strong>Statut :</strong> ${application.status}</p>
      ${
        application.link 
        ? `<p><a href="${application.link}" target="_blank">Voir l'offre</a></p>` 
        : ""
      }
      <button class="delete-btn" onclick="deleteApplication(${index})">Supprimer</button>
    `;

    applicationList.appendChild(div);
  });
}

function deleteApplication(index) {
  applications.splice(index, 1);
  saveApplications();
  displayApplications();
  updateDashboard();
}

function updateDashboard() {
  document.getElementById("total").textContent = applications.length;

  const relances = applications.filter(app => app.status === "À relancer").length;
  const entretiens = applications.filter(app => app.status === "Entretien").length;

  document.getElementById("relances").textContent = relances;
  document.getElementById("entretiens").textContent = entretiens;
}

function generateAdvice() {
  const adviceList = [
    "Pense à relancer les entreprises après 5 à 7 jours sans réponse.",
    "Priorise les offres qui correspondent à ton projet professionnel.",
    "Personnalise chaque candidature avec quelques phrases adaptées à l’entreprise.",
    "Garde une trace claire de tes candidatures pour ne pas oublier les relances.",
    "Mets en avant tes expériences en gestion, organisation et relation humaine.",
    "Un bon suivi peut faire la différence entre une candidature oubliée et un entretien."
  ];

  const randomIndex = Math.floor(Math.random() * adviceList.length);
  document.getElementById("aiAdvice").textContent = adviceList[randomIndex];
}

displayApplications();
updateDashboard();
