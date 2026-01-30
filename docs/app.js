const state = {
  datasets: [],
  filters: {
    search: "",
    category: "All",
    format: "All",
    access: "All",
    license: "All",
    quick: null,
  },
};

const searchInput = document.getElementById("search");
const categorySelect = document.getElementById("category");
const formatSelect = document.getElementById("format");
const accessSelect = document.getElementById("access");
const licenseSelect = document.getElementById("license");
const datasetBody = document.getElementById("dataset-body");
const resultsMeta = document.getElementById("results-meta");
const quickFilters = document.getElementById("quick-filters");

const datasetCount = document.getElementById("dataset-count");
const categoryCount = document.getElementById("category-count");
const formatCount = document.getElementById("format-count");

const quickFilterOptions = [
  { label: "NetCDF", predicate: (d) => d.format.toLowerCase().includes("netcdf") },
  { label: "GeoTiff", predicate: (d) => d.format.toLowerCase().includes("geotiff") },
  { label: "API key", predicate: (d) => d.access_conditions.toLowerCase().includes("api key") },
  { label: "NCI access", predicate: (d) => d.access_conditions.toLowerCase().includes("nci") },
  { label: "Free access", predicate: (d) => d.access_conditions.toLowerCase().includes("free") },
];

function uniqueValues(values) {
  return ["All", ...Array.from(new Set(values)).filter(Boolean).sort()];
}

function splitFormats(format) {
  return format
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
}

function populateSelect(select, values) {
  select.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function renderQuickFilters() {
  quickFilters.innerHTML = "";
  quickFilterOptions.forEach((option) => {
    const button = document.createElement("button");
    button.className = "chip";
    button.type = "button";
    button.textContent = option.label;
    button.addEventListener("click", () => {
      state.filters.quick = state.filters.quick === option.label ? null : option.label;
      render();
    });
    if (state.filters.quick === option.label) {
      button.classList.add("active");
    }
    quickFilters.appendChild(button);
  });
}

function applyFilters(dataset) {
  const query = state.filters.search.toLowerCase();
  const matchesSearch =
    !query ||
    [
      dataset.name,
      dataset.variables,
      dataset.method,
      dataset.format,
      dataset.category,
      dataset.access_conditions,
    ]
      .join(" ")
      .toLowerCase()
      .includes(query);

  const matchesCategory =
    state.filters.category === "All" || dataset.category === state.filters.category;
  const matchesFormat =
    state.filters.format === "All" || dataset.format.includes(state.filters.format);
  const matchesAccess =
    state.filters.access === "All" || dataset.access_conditions === state.filters.access;
  const matchesLicense =
    state.filters.license === "All" || dataset.license === state.filters.license;

  const quickFilter = quickFilterOptions.find((q) => q.label === state.filters.quick);
  const matchesQuick = quickFilter ? quickFilter.predicate(dataset) : true;

  return (
    matchesSearch &&
    matchesCategory &&
    matchesFormat &&
    matchesAccess &&
    matchesLicense &&
    matchesQuick
  );
}

function renderTable(rows) {
  datasetBody.innerHTML = "";
  rows.forEach((dataset) => {
    const tr = document.createElement("tr");
    const details = `
      <div class="details">
        <strong>Variables:</strong> ${dataset.variables || "-"}<br />
        <strong>Method:</strong> ${dataset.method || "-"}<br />
        <strong>Spatial domain:</strong> ${dataset.spatial_domain || "-"}<br />
        <strong>Update frequency:</strong> ${dataset.update_frequency || "-"}
      </div>
    `;

    tr.innerHTML = `
      <td><a href="${dataset.source_url}" target="_blank" rel="noopener">${dataset.name}</a></td>
      <td>${dataset.category || "-"}</td>
      <td>${dataset.resolution || "-"}</td>
      <td>${dataset.format || "-"}</td>
      <td>${dataset.access_conditions || "-"}</td>
      <td>${dataset.temporal_coverage || "-"}</td>
      <td>${details}</td>
    `;

    datasetBody.appendChild(tr);
  });
}

function render() {
  const filtered = state.datasets.filter(applyFilters);
  renderTable(filtered);
  resultsMeta.textContent = `${filtered.length} result${filtered.length === 1 ? "" : "s"}`;
  renderQuickFilters();
}

function attachEvents() {
  searchInput.addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    render();
  });

  categorySelect.addEventListener("change", (event) => {
    state.filters.category = event.target.value;
    render();
  });

  formatSelect.addEventListener("change", (event) => {
    state.filters.format = event.target.value;
    render();
  });

  accessSelect.addEventListener("change", (event) => {
    state.filters.access = event.target.value;
    render();
  });

  licenseSelect.addEventListener("change", (event) => {
    state.filters.license = event.target.value;
    render();
  });
}

async function init() {
  const response = await fetch("./data/datasets.json");
  const payload = await response.json();
  state.datasets = payload.datasets;

  datasetCount.textContent = state.datasets.length.toString();

  const categories = uniqueValues(state.datasets.map((d) => d.category));
  const formats = uniqueValues(state.datasets.flatMap((d) => splitFormats(d.format)));
  const access = uniqueValues(state.datasets.map((d) => d.access_conditions));
  const licenses = uniqueValues(state.datasets.map((d) => d.license).filter(Boolean));

  categoryCount.textContent = (categories.length - 1).toString();
  formatCount.textContent = (formats.length - 1).toString();

  populateSelect(categorySelect, categories);
  populateSelect(formatSelect, formats);
  populateSelect(accessSelect, access);
  populateSelect(licenseSelect, ["All", ...licenses]);

  attachEvents();
  render();
}

init();
