// PlaylistWise AI - shared client logic
(function () {
  const API_BASE = "http://127.0.0.1:8000";

  window.PW = {
    API: API_BASE.replace(/\/$/, "") + "/api",
    token: () => localStorage.getItem("pw_token"),

    user: () => {
      try {
        return JSON.parse(localStorage.getItem("pw_user") || "null");
      } catch {
        return null;
      }
    },

    setAuth: (token, user) => {
      localStorage.setItem("pw_token", token);
      localStorage.setItem("pw_user", JSON.stringify(user));
    },

    logout: () => {
      localStorage.removeItem("pw_token");
      localStorage.removeItem("pw_user");
      window.location.href = "/";
    },

    requireAuth: () => {
      if (!localStorage.getItem("pw_token")) {
        window.location.href = "/login.html";
        return false;
      }
      return true;
    },

    api: async (path, opts = {}) => {
      const headers = {
        "Content-Type": "application/json",
        ...(opts.headers || {}),
      };
      const tok = localStorage.getItem("pw_token");
      if (tok) headers.Authorization = "Bearer " + tok;
      const res = await fetch(API_BASE.replace(/\/$/, "") + "/api" + path, {
        ...opts,
        headers,
      });
      if (!res.ok) {
        let err = "Request failed";
        try {
          const j = await res.json();
          err = j.detail || err;
        } catch {}
        throw new Error(err);
      }
      if (res.status === 204) return null;
      return res.json();
    },

    toast: (msg, type = "info") => {
      let c = document.getElementById("toast-container");
      if (!c) {
        c = document.createElement("div");
        c.id = "toast-container";
        document.body.appendChild(c);
      }
      const t = document.createElement("div");
      t.className = "toast " + type;

      // 🛡️ Lock this specific toast with a unique custom attribute
      t.setAttribute("data-permanent", "true");

      const icons = {
        success: "ph-check-circle",
        error: "ph-x-circle",
        info: "ph-info",
      };
      t.innerHTML = `<i class="ph ${icons[type] || icons.info}"></i><span>${msg}</span>`;
      c.appendChild(t);

      setTimeout(() => {
        t.style.opacity = "0";
        t.style.transition = "opacity 0.3s";
        setTimeout(() => t.remove(), 300);
      }, 10000); // 10 seconds
    },

    // Tiny markdown renderer (headings, bold, italic, inline code, code blocks, lists, paragraphs, links)
    md: (text) => {
      let html = String(text || "");
      // Escape HTML
      html = html
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      // Code blocks ```lang\n...\n```
      html = html.replace(
        /```(\w+)?\n([\s\S]*?)```/g,
        (_, lang, code) => `<pre><code>${code}</code></pre>`,
      );
      // Headings
      html = html.replace(/^### (.*$)/gm, "<h3>$1</h3>");
      html = html.replace(/^## (.*$)/gm, "<h2>$1</h2>");
      html = html.replace(/^# (.*$)/gm, "<h1>$1</h1>");
      // Bold and italic
      html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
      html = html.replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>");
      // Inline code
      html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
      // Links [text](url)
      html = html.replace(
        /\[([^\]]+)\]\(([^)]+)\)/g,
        '<a href="$2" target="_blank">$1</a>',
      );
      // Lists
      html = html.replace(/^\s*[-*] (.+)$/gm, "<li>$1</li>");
      html = html.replace(/(<li>[\s\S]*?<\/li>)/g, (m) => "<ul>" + m + "</ul>");
      html = html.replace(/<\/ul>\s*<ul>/g, "");
      // Paragraphs (blank-line separated chunks that aren't already block elements)
      const blocks = html.split(/\n{2,}/).map((b) => {
        if (/^\s*<(h\d|ul|ol|pre|li)/.test(b)) return b;
        return "<p>" + b.replace(/\n/g, "<br>") + "</p>";
      });
      return blocks.join("\n");
    },
    fmtDate: (iso) => {
      try {
        return new Date(iso).toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
      } catch {
        return "";
      }
    },
    qs: (k) => new URLSearchParams(window.location.search).get(k),
    initials: (name) =>
      (name || "U")
        .trim()
        .split(/\s+/)
        .map((p) => p[0])
        .slice(0, 2)
        .join("")
        .toUpperCase(),
  };

  // Inject base topbar avatar color if user
  document.addEventListener("DOMContentLoaded", () => {
    const u = PW.user();
    document.querySelectorAll("[data-user-avatar]").forEach((el) => {
      if (u) {
        el.textContent = PW.initials(u.full_name);
        el.style.background =
          u.avatar_color ||
          "linear-gradient(135deg, var(--primary), var(--secondary))";
      }
    });
    document.querySelectorAll("[data-user-name]").forEach((el) => {
      if (u) el.textContent = u.full_name;
    });
    document.querySelectorAll("[data-logout]").forEach((el) =>
      el.addEventListener("click", (e) => {
        e.preventDefault();
        PW.logout();
      }),
    );
  });
})();
