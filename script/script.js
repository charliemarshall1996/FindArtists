
//Fetch changelog
fetch('CHANGELOG.md')
  .then(response => response.text())
  .then(text => {
    document.getElementById('changeLog').innerHTML = marked.parse(text);
  });
  