ymaps.ready(init);

function init() {

    var myMap = new ymaps.Map('map', {
        center: [37.60, 55.77],
        zoom: 13,
        controls: ['mediumMapDefaultSet'],
    }, {
        restrictMapArea: [
            [37.175,55.453],
            [38.019,56.001]
        ]
    });

    var routePanelControl = new ymaps.control.RoutePanel({
        options: {
            showHeader: true,
            title: 'Вызов такси',
            routePanelTypes: {taxi: true},
            maxWidth: '210px'
        }
    });

    routePanelControl.routePanel.state.set({
        type: "taxi",
    });
    var zoomControl = new ymaps.control.ZoomControl({
        options: {
            size: 'small',
            float: 'none',
            position: {
                bottom: 145,
                right: 10
            }
        }
    });
    
    myMap.controls.add(routePanelControl).add(zoomControl);

    myMap.geoObjects.add(polygon);
    myMap.setBounds(polygon.geometry.getBounds());
}

var Cal = function(divId) {
    this.divId = divId;
    this.DaysOfWeek = [
      'Пн',
      'Вт',
      'Ср',
      'Чтв',
      'Птн',
      'Суб',
      'Вск'
    ];
    this.Months =['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    var d = new Date();
    this.currMonth = d.getMonth();
    this.currYear = d.getFullYear();
    this.currDay = d.getDate();
};

Cal.prototype.nextMonth = function() {
    if ( this.currMonth == 11 ) {
      this.currMonth = 0;
      this.currYear = this.currYear + 1;
    }
    else {
      this.currMonth = this.currMonth + 1;
    }
    this.showcurr();
};
  
Cal.prototype.previousMonth = function() {
    if ( this.currMonth == 0 ) {
      this.currMonth = 11;
      this.currYear = this.currYear - 1;
    }
    else {
      this.currMonth = this.currMonth - 1;
    }
    this.showcurr();
  
};
  
Cal.prototype.showcurr = function() {
    this.showMonth(this.currYear, this.currMonth);

    var normalDays = document.querySelectorAll("#divCal .normal");
    for (var i = 0; i < normalDays.length; i++) {
      normalDays[i].addEventListener("click", function() {
        var selectedDay = this.innerHTML;
        document.getElementById("selected-date").innerHTML = "Вы выбрали: " + selectedDay + " число";
      });
    }

    var todayDate = document.querySelector("#divCal .today");
    todayDate.addEventListener("click", function() {
      var selectedDay = this.innerHTML;
      document.getElementById("selected-date").innerHTML = "Вы выбрали: " + selectedDay + " число";
    }); 

    var nextDays = document.querySelectorAll("#divCal .next-days");
    for (var i = 0; i < nextDays.length; i++) {
      nextDays[i].addEventListener("click", function() {
        var selectedDay = this.innerHTML;
        document.getElementById("selected-date").innerHTML = "Вы выбрали: " + selectedDay + " число";
      });
    }
};
  
Cal.prototype.showMonth = function(y, m) {
    var d = new Date() 
    , firstDayOfMonth = new Date(y, m, 7).getDay()
    , lastDateOfMonth =  new Date(y, m+1, 0).getDate()
    , lastDayOfLastMonth = m == 0 ? new Date(y-1, 11, 0).getDate() : new Date(y, m, 0).getDate();
    var html = '<table>';
    html += '<thead><tr>';
    html += '<td colspan="7">' + this.Months[m] + ' ' + y + '</td>';
    html += '</tr></thead>';
    html += '<tr class="days">';
    for(var i=0; i < this.DaysOfWeek.length;i++) {
      html += '<td>' + this.DaysOfWeek[i] + '</td>';
    }
    html += '</tr>';
    var i=1;
    do {
      var dow = new Date(y, m, i).getDay();
      if ( dow == 1 ) {
        html += '<tr>';
      }

      else if ( i == 1 ) {
        html += '<tr>';
        var k = lastDayOfLastMonth - firstDayOfMonth+1;
        for(var j=0; j < firstDayOfMonth; j++) {
          html += '<td class="not-current">' + k + '</td>';
          k++;
        }
      }
      
      var chk = new Date();
        var chkY = chk.getFullYear();
        var chkM = chk.getMonth();

        if (chkY == this.currYear && chkM == this.currMonth && i == this.currDay) {
            html += '<td class="today">' + i + '</td>'; 
        } else if ((chkY == this.currYear && chkM == this.currMonth && i > this.currDay) && (i <= this.currDay + 6)) {
            html += '<td class="next-days">' + i + '</td>';
        } else {
            html += '<td class="normal">' + i + '</td>';
        }

      
      if ( dow == 0 ) {
        html += '</tr>';
      }
      
      else if ( i == lastDateOfMonth ) {
        var k=1;
        for(dow; dow < 7; dow++) {
          html += '<td class="not-current">' + k + '</td>';
          k++;
        }
      }
      i++;
    }while(i <= lastDateOfMonth);
    
    html += '</table>';
    
    document.getElementById(this.divId).innerHTML = html;
  
};


document.getElementById('show-chart-button').addEventListener('click', function() {
  var data = {
      labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00'],
      datasets: [{
          label: 'Примерный график',
          data: [12, 19, 3, 5, 2, 3],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
      }]
  };

  var options = {
      scales: {
          y: {
              beginAtZero: true
          }
      }
  };

  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: options
  });
});
  
window.onload = function() {
    
    var c = new Cal("divCal");			
    c.showcurr();
    
    getId('btnNext').onclick = function() {
      c.nextMonth();
    };
    getId('btnPrev').onclick = function() {
      c.previousMonth();
    };
  
}
  
  
function getId(id) {
    return document.getElementById(id);
  
}

function showCurrentTime() {
    var currentTimeElement = document.getElementById('current-time');
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();
    var timeString = hours + ':' + (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    currentTimeElement.innerHTML = 'Текущее время: ' + timeString;
}

showCurrentTime();

setInterval(showCurrentTime, 1000);


