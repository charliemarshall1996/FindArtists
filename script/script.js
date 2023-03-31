
//Fetch changelog
fetch('../CHANGELOG.md')
  .then(response => response.text())
  .then(text => {
    document.getElementById('changelog').innerHTML = marked.parse(text);
  });
