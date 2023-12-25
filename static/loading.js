document.addEventListener('DOMContentLoaded', function () {
    const loadingBar = document.getElementById('loading-bar');
    const loadingText = document.getElementById('loading-text');
    
    setTimeout(() => {
        loadingBar.style.width = '100%';
    }, 3000);
    
    // fetch from home-async, then set the window's html to the response content
    fetch('/home-async').then((response) => {
        loadingText.innerText = 'Profile loading complete!';
        return response.text();
    }).then((html) => {
        setTimeout(() => {
            document.open();
            document.write(html);
            document.close();
        }, 2000);
    }).then(() => {
        window.history.pushState("dashboard", "result-view", "/dashboard")
    });
});