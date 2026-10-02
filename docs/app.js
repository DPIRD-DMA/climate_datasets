const SORTS = [
  { value: "name", label: "Name (A-Z)" },
  { value: "resolution", label: "Resolution (finest first)" },
  { value: "start", label: "Start year (earliest first)" },
];

// Filter key -> select element id and URL query parameter.
const SELECT_FILTERS = {
  timestep: { id: "timestep", param: "step", all: "Any time step" },
  domain: { id: "domain", param: "domain", all: "Any domain" },
  access: { id: "access", param: "access", all: "Any access" },
  format: { id: "format", param: "format", all: "Any format" },
  license: { id: "license", param: "licence", all: "Any licence" },
  category: { id: "category", param: "category", all: "Any category" },
};
const NO_LICENCE = "none";

function defaultFilters() {
  return {
    search: "",
    timestep: "",
    domain: "",
    access: "",
    format: "",
    license: "",
    category: "",
    maxres: "",
    sort: "name",
    tags: new Set(),
  };
}

const state = {
  datasets: [],
  options: {},
  open: new Set(),
  filters: defaultFilters(),
};

const searchInput = document.getElementById("search");
const sortSelect = document.getElementById("sort");
const maxresInput = document.getElementById("maxres");
const clearButton = document.getElementById("clear");
const filterPanel = document.getElementById("filter-panel");
const filterCount = document.getElementById("filter-count");
const tagList = document.getElementById("variable-tags");
const datasetBody = document.getElementById("dataset-body");
const resultsMeta = document.getElementById("results-meta");
const emptyMessage = document.getElementById("empty");
const summary = document.getElementById("summary");
const footerNote = document.getElementById("footer-note");
const selects = Object.fromEntries(
  Object.entries(SELECT_FILTERS).map(([key, { id }]) => [key, document.getElementById(id)])
);

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

function formatPeriod(dataset) {
  return `${dataset.start_year}–${dataset.end_year === null ? "present" : dataset.end_year}`;
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-AU", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
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

function cell(label, content, className) {
  const td = el("td", { className, attrs: { "data-label": label } });
  td.append(content);
  return td;
}

function renderRow(dataset, index) {
  const detailId = `details-${index}`;
  const isOpen = state.open.has(dataset.name);
  const href = safeUrl(dataset.source_url);
  const name = href
    ? el("a", { text: dataset.name, attrs: { href, target: "_blank", rel: "noopener" } })
    : document.createTextNode(dataset.name);

  const toggle = el("button", {
    className: "toggle",
    text: "Details",
    attrs: { type: "button", "aria-expanded": String(isOpen), "aria-controls": detailId },
  });

  const row = el("tr", { className: isOpen ? "row is-open" : "row" });
  row.append(
    cell("Dataset", name, "cell-name"),
    cell("Category", document.createTextNode(dataset.category || "-")),
    cell("Resolution", document.createTextNode(formatResolution(dataset))),
    cell("Period", document.createTextNode(formatPeriod(dataset)), "cell-period"),
    cell("Time steps", pills(dataset.timesteps)),
    cell("Access", pills(dataset.access_types)),
    cell("Licence", licenceBadge(dataset)),
    cell("", toggle, "cell-toggle")
  );

  const detailRow = el("tr", { className: "row-details", attrs: { id: detailId } });
  detailRow.hidden = !isOpen;
  detailRow.append(el("td", { attrs: { colspan: "8" } }, [detailList(dataset)]));

  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    detailRow.hidden = open;
    row.classList.toggle("is-open", !open);
    if (open) state.open.delete(dataset.name);
    else state.open.add(dataset.name);
  });

  return [row, detailRow];
}

function renderTable(rows) {
  datasetBody.replaceChildren(...rows.flatMap((dataset, index) => renderRow(dataset, index)));
}

function maxResolution(filters) {
  const value = parseFloat(filters.maxres);
  return Number.isFinite(value) && value > 0 ? value : null;
}

function matches(dataset, filters) {
  const query = filters.search.trim().toLowerCase();
  if (query) {
    const haystack = [
      dataset.name,
      dataset.variables,
      dataset.method,
      dataset.format,
      dataset.category,
      dataset.access_conditions,
      dataset.variable_tags.join(" "),
    ]
      .join(" ")
      .toLowerCase();
    if (!haystack.includes(query)) return false;
  }
  if (filters.timestep && !dataset.timesteps.includes(filters.timestep)) return false;
  if (filters.domain && dataset.domain !== filters.domain) return false;
  if (filters.access && !dataset.access_types.includes(filters.access)) return false;
  if (filters.format && !dataset.formats.includes(filters.format)) return false;
  if (filters.category && dataset.category !== filters.category) return false;
  if (filters.license === NO_LICENCE && dataset.license) return false;
  if (filters.license && filters.license !== NO_LICENCE && dataset.license !== filters.license) {
    return false;
  }
  const max = maxResolution(filters);
  if (max !== null && !(typeof dataset.resolution_km === "number" && dataset.resolution_km <= max)) {
    return false;
  }
  return [...filters.tags].every((tag) => dataset.variable_tags.includes(tag));
}

function comparator(sort) {
  const byName = (a, b) => a.name.localeCompare(b.name, "en", { sensitivity: "base" });
  if (sort === "resolution") {
    return (a, b) => {
      const x = a.resolution_km;
      const y = b.resolution_km;
      if (x === y) return byName(a, b);
      if (x === null) return 1;
      if (y === null) return -1;
      return x - y || byName(a, b);
    };
  }
  if (sort === "start") return (a, b) => a.start_year - b.start_year || byName(a, b);
  return byName;
}

function activeFilterCount(filters) {
  const selected = Object.keys(SELECT_FILTERS).filter((key) => filters[key]).length;
  return selected + (maxResolution(filters) !== null ? 1 : 0) + filters.tags.size;
}

function readUrl() {
  const params = new URLSearchParams(location.search);
  const filters = defaultFilters();
  filters.search = params.get("q") || "";
  Object.entries(SELECT_FILTERS).forEach(([key, { param }]) => {
    const value = params.get(param);
    if (value && state.options[key].some((option) => option.value === value)) {
      filters[key] = value;
    }
  });
  const maxres = params.get("maxres");
  if (maxres && Number.isFinite(parseFloat(maxres)) && parseFloat(maxres) > 0) {
    filters.maxres = maxres;
  }
  const sort = params.get("sort");
  if (SORTS.some((option) => option.value === sort)) filters.sort = sort;
  params
    .getAll("tag")
    .filter((tag) => state.options.tags.includes(tag))
    .forEach((tag) => filters.tags.add(tag));
  return filters;
}

function writeUrl() {
  const filters = state.filters;
  const params = new URLSearchParams();
  if (filters.search) params.set("q", filters.search);
  Object.entries(SELECT_FILTERS).forEach(([key, { param }]) => {
    if (filters[key]) params.set(param, filters[key]);
  });
  if (maxResolution(filters) !== null) params.set("maxres", filters.maxres);
  if (filters.sort !== "name") params.set("sort", filters.sort);
  state.options.tags
    .filter((tag) => filters.tags.has(tag))
    .forEach((tag) => params.append("tag", tag));
  const query = params.toString();
  history.replaceState(null, "", query ? `?${query}` : location.pathname);
}

function syncControls() {
  const filters = state.filters;
  searchInput.value = filters.search;
  sortSelect.value = filters.sort;
  maxresInput.value = filters.maxres;
  Object.keys(SELECT_FILTERS).forEach((key) => {
    selects[key].value = filters[key];
  });
  tagList.querySelectorAll("button").forEach((button) => {
    button.setAttribute("aria-pressed", String(filters.tags.has(button.dataset.tag)));
  });
}

function render() {
  const filters = state.filters;
  const rows = state.datasets.filter((dataset) => matches(dataset, filters)).sort(comparator(filters.sort));
  renderTable(rows);
  resultsMeta.textContent = `${rows.length} of ${state.datasets.length} datasets`;
  emptyMessage.hidden = rows.length > 0;
  const active = activeFilterCount(filters);
  filterCount.textContent = active ? `(${active} active)` : "";
  clearButton.hidden = active === 0 && !filters.search && filters.sort === "name";
  writeUrl();
}

function fillSelect(select, allLabel, options) {
  select.replaceChildren(
    el("option", { text: allLabel, attrs: { value: "" } }),
    ...options.map(({ value, label }) => el("option", { text: label, attrs: { value } }))
  );
}

function inVocabOrder(vocabValues, used) {
  return vocabValues.filter((value) => used.has(value));
}

function buildOptions(vocab) {
  const datasets = state.datasets;
  const plain = (values) => values.map((value) => ({ value, label: value }));
  const licences = [...new Set(datasets.map((d) => d.license).filter(Boolean))].sort();
  const licenceOptions = plain(licences);
  if (datasets.some((d) => !d.license)) licenceOptions.push({ value: NO_LICENCE, label: "Not stated" });

  state.options = {
    timestep: plain(inVocabOrder(vocab.timesteps, new Set(datasets.flatMap((d) => d.timesteps)))),
    domain: plain(inVocabOrder(vocab.domain, new Set(datasets.map((d) => d.domain)))),
    access: plain(inVocabOrder(vocab.access_types, new Set(datasets.flatMap((d) => d.access_types)))),
    format: plain(inVocabOrder(vocab.formats, new Set(datasets.flatMap((d) => d.formats)))),
    license: licenceOptions,
    category: plain([...new Set(datasets.map((d) => d.category))].sort()),
    tags: inVocabOrder(vocab.variable_tags, new Set(datasets.flatMap((d) => d.variable_tags))),
  };
}

function buildControls() {
  Object.entries(SELECT_FILTERS).forEach(([key, { all }]) => {
    fillSelect(selects[key], all, state.options[key]);
  });
  sortSelect.replaceChildren(
    ...SORTS.map(({ value, label }) => el("option", { text: label, attrs: { value } }))
  );
  tagList.replaceChildren(
    ...state.options.tags.map((tag) =>
      el("button", {
        className: "chip",
        text: tag,
        attrs: { type: "button", "aria-pressed": "false", "data-tag": tag },
      })
    )
  );
}

function renderSummary() {
  const counts = state.options.access.map(
    ({ value }) => `${value} ${state.datasets.filter((d) => d.access_types.includes(value)).length}`
  );
  summary.textContent = `${state.datasets.length} datasets. Access: ${counts.join(", ")}.`;

  const dates = state.datasets.map((d) => d.last_checked).sort();
  const first = formatDate(dates[0]);
  const last = formatDate(dates[dates.length - 1]);
  footerNote.textContent =
    first === last ? `Entries last checked ${first}.` : `Entries last checked between ${first} and ${last}.`;
}

function attachEvents() {
  searchInput.addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    render();
  });
  sortSelect.addEventListener("change", (event) => {
    state.filters.sort = event.target.value;
    render();
  });
  maxresInput.addEventListener("input", (event) => {
    state.filters.maxres = event.target.value.trim();
    render();
  });
  Object.keys(SELECT_FILTERS).forEach((key) => {
    selects[key].addEventListener("change", (event) => {
      state.filters[key] = event.target.value;
      render();
    });
  });
  tagList.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-tag]");
    if (!button) return;
    const tag = button.dataset.tag;
    if (state.filters.tags.has(tag)) state.filters.tags.delete(tag);
    else state.filters.tags.add(tag);
    button.setAttribute("aria-pressed", String(state.filters.tags.has(tag)));
    render();
  });
  clearButton.addEventListener("click", () => {
    state.filters = defaultFilters();
    syncControls();
    render();
  });
}

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

async function init() {
  try {
    const [payload, vocab] = await Promise.all([
      fetchJson("./data/datasets.json"),
      fetchJson("./data/vocab.json"),
    ]);
    state.datasets = payload.datasets;
    buildOptions(vocab);
  } catch (error) {
    resultsMeta.textContent = "Could not load the dataset registry.";
    return;
  }

  buildControls();
  renderSummary();
  state.filters = readUrl();
  syncControls();
  if (window.matchMedia("(max-width: 720px)").matches && activeFilterCount(state.filters) === 0) {
    filterPanel.open = false;
  }
  attachEvents();
  render();
}

init();
