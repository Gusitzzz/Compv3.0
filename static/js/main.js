function updateClock() {
    const now = new Date();
    const str = now.getFullYear() + '-' +
              (now.getMonth()+1).toString().padStart(2,'0') + '-' +
              now.getDate().toString().padStart(2,'0') + ' ' +
              now.getHours().toString().padStart(2,'0') + ':' +
              now.getMinutes().toString().padStart(2,'0') + ':' +
              now.getSeconds().toString().padStart(2,'0');
    document.getElementById('clock').innerText = str;
}
setInterval(updateClock, 1000);
updateClock();

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
}