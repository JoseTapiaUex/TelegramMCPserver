const API_BASE_URL = window.API_BASE_URL || "http://localhost:8000";
const POSTS_ENDPOINT = `${API_BASE_URL}/api/posts`;
const REFRESH_INTERVAL_MS = 5 * 60 * 1000;

const postsContainer = document.querySelector("#postsContainer");
const postTemplate = document.querySelector("#postTemplate");
const refreshButton = document.querySelector("#refreshButton");

async function fetchPosts() {
  try {
    const response = await fetch(POSTS_ENDPOINT);
    if (!response.ok) {
      throw new Error(`API responded with ${response.status}`);
    }
    const data = await response.json();
    return Array.isArray(data.items) ? data.items : [];
  } catch (error) {
    console.error("Unable to fetch posts", error);
    return [];
  }
}

function getProvider(post) {
  if (post.provider) {
    return post.provider;
  }
  try {
    return new URL(post.source_url).hostname;
  } catch (error) {
    return "Fuente desconocida";
  }
}

function renderPosts(posts) {
  postsContainer.innerHTML = "";
  if (posts.length === 0) {
    postsContainer.innerHTML = '<p class="empty-state">No hay publicaciones disponibles todavía.</p>';
    return;
  }

  const fragment = document.createDocumentFragment();
  posts.forEach((post) => {
    const element = postTemplate.content.firstElementChild.cloneNode(true);

    const imageWrapper = element.querySelector(".image-wrapper");
    imageWrapper.innerHTML = "";

    if (post.image_url) {
      const image = document.createElement("img");
      image.src = post.image_url;
      image.alt = post.title || "Imagen destacada";
      image.loading = "lazy";
      imageWrapper.appendChild(image);
    } else {
      imageWrapper.classList.add("no-image");
      imageWrapper.textContent = "Sin imagen";
    }

    element.querySelector(".post-title").textContent = post.title;
    element.querySelector(".post-summary").textContent = post.summary;
    element.querySelector(".post-link").href = post.source_url;
    element.querySelector(".post-link").setAttribute("aria-label", `Abrir ${post.title}`);

    element.querySelector(".provider").textContent = getProvider(post);
    element.querySelector(".release-date").textContent = post.release_date || "Fecha desconocida";

    fragment.appendChild(element);
  });

  postsContainer.appendChild(fragment);
}

async function refresh() {
  const posts = await fetchPosts();
  renderPosts(posts);
}

refreshButton?.addEventListener("click", refresh);

refresh();
setInterval(refresh, REFRESH_INTERVAL_MS);
