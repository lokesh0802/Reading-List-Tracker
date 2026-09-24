import { API_BASE_URL } from "./config.js";

const STATUSES = [
  { value: "to-read", label: "To read" },
  { value: "reading", label: "Reading" },
  { value: "done", label: "Done" },
];

const form = document.querySelector("#book-form");
const message = document.querySelector("#message");
const bookList = document.querySelector("#book-list");
const statusFilter = document.querySelector("#status-filter");
const submitButton = form.querySelector('button[type="submit"]');

function apiUrl(path) {
  return `${API_BASE_URL.replace(/\/$/, "")}${path}`;
}

async function apiRequest(path, options = {}) {
  const response = await fetch(apiUrl(path), options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "The request could not be completed.");
  }

  return data;
}

function showMessage(text, type) {
  message.textContent = text;
  message.className = `message ${type}`;
}

function createStatusSelect(book) {
  const select = document.createElement("select");
  select.setAttribute("aria-label", `Change status for ${book.title}`);

  STATUSES.forEach(({ value, label }) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    option.selected = book.status === value;
    select.append(option);
  });

  select.addEventListener("change", async () => {
    select.disabled = true;

    try {
      await apiRequest(`/api/books/${encodeURIComponent(book.id)}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: select.value }),
      });
      await refreshBooksAndStats();
      showMessage(`Updated “${book.title}” successfully.`, "success");
    } catch (error) {
      select.value = book.status;
      select.disabled = false;
      showMessage(error.message, "error");
    }
  });

  return select;
}

function renderBooks(books) {
  bookList.replaceChildren();

  if (books.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No books found.";
    bookList.append(emptyState);
    return;
  }

  books.forEach((book) => {
    const row = document.createElement("article");
    row.className = "book-row";

    const details = document.createElement("div");
    const title = document.createElement("h3");
    const author = document.createElement("p");

    title.textContent = book.title;
    author.textContent = `by ${book.author}`;
    details.append(title, author);
    row.append(details, createStatusSelect(book));
    bookList.append(row);
  });
}

function renderStats(stats) {
  document.querySelector("#to-read-count").textContent = stats["to-read"];
  document.querySelector("#reading-count").textContent = stats.reading;
  document.querySelector("#done-count").textContent = stats.done;
}

async function refreshBooksAndStats() {
  const filter = statusFilter.value;
  const booksPath = filter
    ? `/api/books?status=${encodeURIComponent(filter)}`
    : "/api/books";

  const [books, stats] = await Promise.all([
    apiRequest(booksPath),
    apiRequest("/api/stats"),
  ]);

  renderBooks(books);
  renderStats(stats);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  submitButton.disabled = true;

  const formData = new FormData(form);
  const bookData = {
    title: formData.get("title"),
    author: formData.get("author"),
    status: formData.get("status"),
  };

  try {
    const book = await apiRequest("/api/books", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookData),
    });
    form.reset();
    await refreshBooksAndStats();
    showMessage(`Added “${book.title}” successfully.`, "success");
  } catch (error) {
    showMessage(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});

statusFilter.addEventListener("change", async () => {
  try {
    await refreshBooksAndStats();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

refreshBooksAndStats().catch((error) => {
  showMessage(error.message, "error");
});
