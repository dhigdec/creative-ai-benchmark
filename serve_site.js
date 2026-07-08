const http = require("http"), fs = require("fs"), path = require("path");
const ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads";
const MIME = {".html":"text/html",".json":"application/json",".css":"text/css",".js":"text/javascript"};
http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p === "/") p = "/Adobe_Connector_Doable_Tasks.html";
  const file = path.join(ROOT, p);
  fs.readFile(file,(err,buf)=>{
    if(err){res.writeHead(404);res.end("not found");return}
    res.writeHead(200,{"Content-Type":MIME[path.extname(file)]||"application/octet-stream"});
    res.end(buf);
  });
}).listen(8765,()=>console.log("serving on 8765"));
