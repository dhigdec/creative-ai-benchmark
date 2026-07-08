// Minimal static server for Doable_Tasks.html
const http = require("http");
const fs = require("fs");
const path = require("path");
const ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads";
const PORT = 8803;
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p === "/" || p === "") p = "/Doable_Tasks.html";
  const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
    res.writeHead(404); res.end("not found"); return;
  }
  const ext = path.extname(fp).toLowerCase();
  const ct = { ".html": "text/html", ".json": "application/json", ".csv": "text/csv",
    ".js": "text/javascript", ".png": "image/png", ".jpg": "image/jpeg", ".pdf": "application/pdf" }[ext] || "application/octet-stream";
  res.writeHead(200, { "Content-Type": ct });
  fs.createReadStream(fp).pipe(res);
}).listen(PORT, () => console.log("doable server on http://localhost:" + PORT));
