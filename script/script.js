  import fs from "fs";
  import parseMD from 'parse-md';
  
  // Get the changelog content
  const changelog = fs.readFileSync('./CHANGELOG.md', 'utf8');
  
  // Parse the markdown
  const {metadata, content} = parseMD(changelog);
  
  console.log(metadata)

  // Display the changelog
  document.getElementById('changeLog').innerHTML = content;