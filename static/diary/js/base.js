document.addEventListener('DOMContentLoaded', function() {
    function updateTime() {
        const now = new Date();

        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const dateString = `${year}年${month}月${day}日`;
        const timeString = `${hours}時${minutes}分${seconds}秒`;
        const dateTimeString = `${dateString} ${timeString}`;
        document.getElementById('clock').textContent = dateTimeString;
    }
    updateTime();
    setInterval(updateTime, 1000); 
});