(function () {
  // 1. Gráfico de Série Temporal: Empréstimos por Mês (Chart.js - Barras)
  const elMes = document.getElementById("dados-mes");
  const canvasMes = document.getElementById("graf-mes");
  if (elMes && canvasMes && typeof Chart !== "undefined") {
    const dadosMes = JSON.parse(elMes.textContent);
    if (dadosMes.length > 0) {
      new Chart(canvasMes, {
        type: "bar",
        data: {
          labels: dadosMes.map((d) => d.mes),
          datasets: [
            {
              label: "Empréstimos",
              data: dadosMes.map((d) => d.total),
              backgroundColor: "#4f46e5",
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { precision: 0 },
            },
          },
        },
      });
    }
  }

  // 2. Gráfico de Distribuição: Empréstimos em Aberto vs Devolvidos (Chart.js - Rosca)
  const elDist = document.getElementById("dados-distribuicao");
  const canvasDist = document.getElementById("graf-distribuicao");
  if (elDist && canvasDist && typeof Chart !== "undefined") {
    const dadosDist = JSON.parse(elDist.textContent);
    const soma = dadosDist.reduce((acc, item) => acc + item.total, 0);
    if (soma > 0) {
      new Chart(canvasDist, {
        type: "doughnut",
        data: {
          labels: dadosDist.map((d) => d.status),
          datasets: [
            {
              data: dadosDist.map((d) => d.total),
              backgroundColor: ["#f59e0b", "#10b981"],
              borderWidth: 2,
              borderColor: "#ffffff",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" },
          },
        },
      });
    }
  }
})();
