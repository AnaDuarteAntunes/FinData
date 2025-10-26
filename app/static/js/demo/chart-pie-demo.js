// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart - CON DATOS REALES Y COLORES FIJOS POR CATEGORÍA
var ctx = document.getElementById("myPieChart");

// Mapeo de categorías a colores (sin Educación)
var categoryColors = {
    'Alimentación': '#4e73df',
    'Transporte': '#1cc88a',
    'Vivienda': '#36b9cc',
    'Ocio': '#f6c23e',
    'Salud': '#e74a3b',
    'Ropa': '#858796',
    'Servicios': '#5a5c69',
    'Mascotas': '#2e59d9',
    'Otros': '#17a673'
};

var categoryColorsHover = {
    'Alimentación': '#2e59d9',
    'Transporte': '#17a673',
    'Vivienda': '#2c9faf',
    'Ocio': '#dda20a',
    'Salud': '#be2617',
    'Ropa': '#6c6e7e',
    'Servicios': '#484a54',
    'Mascotas': '#224aba',
    'Otros': '#0e7d57'
};

// Filtrar categorías (eliminar Educación si existe)
var labels = window.chartData.categoryLabels.filter(cat => cat !== 'Educación');
var amounts = [];
var colors = [];
var hoverColors = [];

// Asignar cantidades y colores según las categorías que existen
for (var i = 0; i < window.chartData.categoryLabels.length; i++) {
    var category = window.chartData.categoryLabels[i];
    if (category !== 'Educación') {
        amounts.push(window.chartData.categoryAmounts[i]);
        colors.push(categoryColors[category] || '#858796');
        hoverColors.push(categoryColorsHover[category] || '#6c6e7e');
    }
}

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: labels,
    datasets: [{
      data: amounts,
      backgroundColor: colors,
      hoverBackgroundColor: hoverColors,
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var label = chart.labels[tooltipItem.index] || '';
          var value = chart.datasets[0].data[tooltipItem.index];
          return label + ': ' + value.toFixed(2) + '€';
        }
      }
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});