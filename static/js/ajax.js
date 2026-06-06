async function refreshData() {
    try {
        const res = await fetch('/api/refresh_data/');
        const data = await res.json();
        
        if (data.units) {
            document.getElementById('temp1').innerText = data.units['Unit 1'].temp.toFixed(1);
            document.getElementById('vib1').innerText = data.units['Unit 1'].vib.toFixed(1);
            document.getElementById('noise1').innerText = data.units['Unit 1'].noise.toFixed(1);
            document.getElementById('status1').innerText = data.units['Unit 1'].status;
            document.getElementById('total_alarms').innerText = data.active_alarms;
            document.getElementById('total_online').innerText = data.online_count + '/' + data.total;
        }
    } catch (e) {
        console.log('Refresh error:', e);
    }
}

setInterval(refreshData, 5000);