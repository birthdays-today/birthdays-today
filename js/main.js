const person = document.getElementById('person');

const today = new Date();
const month = today.toLocaleString('default', { month: 'long' });
const day = today.getDate();

Papa.parse(
  `https://storage.googleapis.com/singtowho.site/csv/${month}_${day}.csv`, {
    download: true,
    header: true,
    complete: function(result) {
      const individual = result.data[Math.floor(Math.random() * result.data.length)];
      person.textContent = individual.name;
      person.href = individual.URL;
    }
  }
);
