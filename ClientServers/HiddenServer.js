const express = require("express");
const app = express();
var { exec, execFile } = require("child_process");
const path = require("path");

app.use(express.static("public"));

app.post("/on", (req, res) => {
  res.send("<p>Hello</p>");
  res.status(200);
  console.log("Request bekommen!");
  exec("cd F:\MinecraftServerRelatedStuff\\MCServer\\NewServer && start lol.bat");
});

app.post("/test", (req, res) => {
  res.send("<p>Hello</p>");
  res.status(200);
  console.log("Test bekommen!");
});

app.listen(2999, console.log("Server listening on port 2999"));
