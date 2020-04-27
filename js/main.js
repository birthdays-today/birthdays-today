const person = document.getElementById('person');

Papa.parse(
  'https://storage.googleapis.com/birthdays_today/csv/birthday.csv', {
    download: true,
    header: true,
    complete: function(result) {
      console.log(result.data);
      console.log(result.data.length);
      console.log(Math.floor(Math.random() * result.data.length));
      const individual = result.data[Math.floor(Math.random() * result.data.length)];
      console.log(individual)

      person.textContent = individual.name;
      person.href = individual.URL;
    }
  });
console.log(data)
//data = Papa.parse('csv_birthday.csv', {download: true, header: true});

individual = data[Math.floor(Math.random() * data.length)];

person.textContent = individual.name;
person.href = individual.URL;
//} else {
//  const errorMessage = document.createElement('marquee');
//  errorMessage.textContent = `Gah, it's not working!`;
//  app.appendChild(errorMessage);
//}
