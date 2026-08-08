console.log("SmartReco tracking initialized");
let pageStartTime = Date.now();
function getCurrentProductId() {

    const productPage =
        document.getElementById("product-page");

    if (!productPage) {
        return null;
    }

    const productId =
        productPage.dataset.productId;

    if (!productId) {
        return null;
    }

    return parseInt(productId);
}
function trackTimeSpent() {

    const seconds =
        Math.floor(
            (Date.now() - pageStartTime) / 1000
        );

    // Ignore very short visits
    if (seconds < 5) {
        return;
    }

    sendTimeSpentEvent(seconds);
}
function sendTimeSpentEvent(seconds) {

    const eventData = {

        event_type: "TIME_SPENT",

        session_id: getSessionId(),

        product_id: getCurrentProductId(),

        event_metadata: JSON.stringify({

            seconds: seconds,

            url: window.location.pathname

        })

    };

    console.log(
        "SENDING TIME_SPENT:",
        eventData
    );

    const blob = new Blob(
        [JSON.stringify(eventData)],
        {
            type: "application/json"
        }
    );

    const sent = navigator.sendBeacon(
        "/events",
        blob
    );

    console.log(
        "TIME_SPENT beacon queued:",
        sent
    );
}
function sendEvent(eventData) {

    fetch("/events", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(eventData)

    })
    .then(response => {

        if (!response.ok) {
            console.log(
                "Event failed:",
                response.status
            );
        }

    })
    .catch(error => {

        console.log(
            "Tracking error:",
            error
        );

    });

}
function getSessionId(){

    let sessionId =
        localStorage.getItem(
            "smartreco_session"
        );


    if(!sessionId){

        sessionId =
            crypto.randomUUID();


        localStorage.setItem(
            "smartreco_session",
            sessionId
        );

    }


    return sessionId;
}
function trackPageView(){

    sendEvent({

        event_type:"PAGE_VIEW",

        session_id:getSessionId()

    });

}
function trackProductView() {

    const productPage =
        document.getElementById("product-page");

    if (!productPage) {
        return;
    }

    const productId =
        productPage.dataset.productId;

    const category =
        productPage.dataset.category;

    sendEvent({

        event_type: "PRODUCT_VIEW",

        session_id: getSessionId(),

        product_id: parseInt(productId),

        category: category

    });
}
function trackSearch() {

    const searchInput =
        document.getElementById("q");

    if (!searchInput) {
        return;
    }

    const query =
        searchInput.value.trim();

    if (!query) {
        return;
    }

    sendEvent({

        event_type: "SEARCH",

        session_id: getSessionId(),

        search_query: query

    });
}
function initializeSearchTracking() {

    const button =
        document.getElementById("apply-filters");

    if (!button) {
        return;
    }

    button.addEventListener("click", () => {

        trackSearch();
        trackFilters();

    });
}
function trackFilters() {

    const category =
        document.getElementById("category")?.value || "";

    const difficulty =
        document.getElementById("difficulty")?.value || "";

    const language =
        document.getElementById("language")?.value || "";

    const minPrice =
        document.getElementById("min_price")?.value || "";

    const maxPrice =
        document.getElementById("max_price")?.value || "";


    // Don't send an event if no filter was selected
    if (
        !category &&
        !difficulty &&
        !language &&
        !minPrice &&
        !maxPrice
    ) {
        return;
    }


    sendEvent({

        event_type: "FILTER",

        session_id: getSessionId(),

        category: category || null,

        event_metadata: JSON.stringify({

            difficulty: difficulty || null,

            language: language || null,

            min_price: minPrice || null,

            max_price: maxPrice || null

        })

    });

}
function trackScrollDepth(depth) {

    sendEvent({

        event_type: "SCROLL_DEPTH",

        session_id: getSessionId(),

        product_id: getCurrentProductId(),

        event_metadata: JSON.stringify({

            depth: depth,

            url: window.location.pathname

        })

    });
}
const scrollThresholds = [25, 50, 75, 90];

const reachedThresholds = new Set();

window.addEventListener("scroll", () => {

    const scrollTop = window.scrollY;

    const documentHeight =
        document.documentElement.scrollHeight;

    const windowHeight =
        window.innerHeight;

    const scrollableHeight =
        documentHeight - windowHeight;

    if (scrollableHeight <= 0) {
        return;
    }

    const scrollPercentage =
        (scrollTop / scrollableHeight) * 100;

    scrollThresholds.forEach((threshold) => {

        if (
            scrollPercentage >= threshold &&
            !reachedThresholds.has(threshold)
        ) {

            reachedThresholds.add(threshold);

            trackScrollDepth(threshold);

        }

    });

});
window.addEventListener("load", () => {

    trackPageView();

    trackProductView();

    initializeSearchTracking();

});


window.addEventListener("beforeunload", () => {

    trackTimeSpent();

});