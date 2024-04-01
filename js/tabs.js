document.addEventListener("DOMContentLoaded", function () {
    // Other initialization code...

    // Determine which tab to open based on URL parameters
    openDefaultTab();
});

function openDefaultTab() {
    const hasParams = window.location.search.length > 0;
    if (hasParams) {
        // If there are any URL parameters, open 'tab2'
        openTab('tab2');
    } else {
        // If there are no URL parameters, open the default tab ('tab1')
        openTab('tab1');
    }
}

function openTab(tabName) {
    // Hide all tab contents
    var tabContents = document.querySelectorAll('.tab-content');
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }

    // Remove "active" class from all tab links
    var tabLinks = document.querySelectorAll('.nav-link');
    for (var i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove('active');
    }

    // Show the selected tab content
    document.getElementById(tabName).style.display = 'block';

    // Add "active" class to the selected tab link
    var activeTabLink = document.querySelector('button.nav-link[onclick="openTab(\'' + tabName + '\')"]');
    if (activeTabLink) {
        activeTabLink.classList.add('active');
    }
}
