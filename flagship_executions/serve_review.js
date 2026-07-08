const http = require("http"), fs = require("fs"), path = require("path");
const ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions";
const MIME = {".html":"text/html",".json":"application/json",".css":"text/css",".js":"text/javascript",
  ".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".svg":"image/svg+xml",
  ".pdf":"application/pdf",".md":"text/plain; charset=utf-8"};
http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p === "/") p = "/Flagship_Review.html";
  const file = path.normalize(path.join(ROOT, p));
  if (!file.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(file,(err,buf)=>{
    if(err){res.writeHead(404);res.end("not found");return}
    res.writeHead(200,{"Content-Type":MIME[path.extname(file).toLowerCase()]||"application/octet-stream"});
    res.end(buf);
  });
}).listen(8801,()=>console.log("flagship review on 8801"));
