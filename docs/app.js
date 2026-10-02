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

function el(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  const { className, text, attrs } = options;
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  Object.entries(attrs || {}).forEach(([name, value]) => node.setAttribute(name, value));
  children.forEach((child) => node.append(child));
  return node;
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:" ? url.href : null;
  } catch {
    return null;
  }
}

function formatResolution(dataset) {
  if (typeof dataset.resolution_km === "number") return `${dataset.resolution_km} km`;
  if (typeof dataset.station_count === "number") {
    return `${dataset.station_count.toLocaleString("en-AU")} stations`;
  }
  return "-";
}

function pills(values) {
  const list = el("ul", { className: "pills" });
  (values || []).forEach((value) => list.append(el("li", { text: value })));
  return list;
}

function licenceBadge(dataset) {
  const licence = (dataset.license || "").trim();
  if (!licence) return el("span", { className: "badge badge--none", text: "Not stated" });
  const noncommercial = /\bNC\b|-NC\b/i.test(licence);
  const sharealike = /\bSA\b|-SA\b/i.test(licence);
  const notes = [];
  if (noncommercial) notes.push("non-commercial use only");
  if (sharealike) notes.push("share-alike: derivatives must use the same licence");
  const badge = el("span", {
    className: `badge${noncommercial ? " badge--nc" : ""}${sharealike ? " badge--sa" : ""}`,
    text: licence,
  });
  if (notes.length) badge.title = `Restriction: ${notes.join("; ")}`;
  return badge;
}

function detailList(dataset) {
  const rows = [
    ["Variables", dataset.variables],
    ["Method", dataset.method],
    ["Resolution", dataset.resolution],
    ["Spatial domain", dataset.spatial_domain],
    ["Temporal coverage", dataset.temporal_coverage],
    ["Update frequency", dataset.update_frequency],
    ["Formats", (dataset.formats || []).join(", ")],
    ["Access", dataset.access_conditions],
    ["Provider contact", dataset.provider_contact],
    ["Last checked", dataset.last_checked],
  ].filter(([, value]) => value);

  const list = el("dl", { className: "details" });
  rows.forEach(([label, value]) => {
    list.append(el("dt", { text: label }), el("dd", { text: value }));
  });
  const href = safeUrl(dataset.source_url);
  if (href) {
    const link = el("a", {
      className: "details__source",
      text: "Open provider page",
      attrs: { href, target: "_blank", rel: "noopener" },
    });
    list.append(el("dt", { text: "Source" }), el("dd", {}, [link]));
  }
  return list;
}

function populateSelect(select, values) {
  select.replaceChildren();
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function renderQuickFilters() {
  quickFilters.replaceChildren();
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

function cell(label, content, className) {
  const td = el("td", { className, attrs: { "data-label": label } });
  td.append(content);
  return td;
}

function renderRow(dataset, index) {
  const detailId = `details-${index}`;
  const href = safeUrl(dataset.source_url);
  const name = href
    ? el("a", { text: dataset.name, attrs: { href, target: "_blank", rel: "noopener" } })
    : document.createTextNode(dataset.name);

  const toggle = el("button", {
    className: "toggle",
    text: "Details",
    attrs: { type: "button", "aria-expanded": "false", "aria-controls": detailId },
  });

  const row = el("tr", { className: "row" });
  row.append(
    cell("Dataset", name, "cell-name"),
    cell("Category", document.createTextNode(dataset.category || "-")),
    cell("Resolution", document.createTextNode(formatResolution(dataset))),
    cell("Time steps", pills(dataset.timesteps)),
    cell("Access", pills(dataset.access_types)),
    cell("Licence", licenceBadge(dataset)),
    cell("", toggle, "cell-toggle")
  );

  const detailRow = el("tr", { className: "row-details", attrs: { id: detailId, hidden: "" } });
  const detailCell = el("td", { attrs: { colspan: "7" } }, [detailList(dataset)]);
  detailRow.append(detailCell);

  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    detailRow.hidden = open;
    row.classList.toggle("is-open", !open);
  });

  return [row, detailRow];
}

function renderTable(rows) {
  datasetBody.replaceChildren(...rows.flatMap((dataset, index) => renderRow(dataset, index)));
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
