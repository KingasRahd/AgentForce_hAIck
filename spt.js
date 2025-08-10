async function getData() {
  try {
    const response = await fetch('http://127.0.0.1:5000/xyz');
    const data = await response.json();
    for (let i = 0; i < data.length; i++) {
      console.log(`Descriptions for ${i} are: ${data[i].description}`);
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
getData();
