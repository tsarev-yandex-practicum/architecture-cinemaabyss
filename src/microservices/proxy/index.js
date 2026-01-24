const express = require('express');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 8000;

const MONOLITH_URL = process.env.MONOLITH_URL;
const MOVIES_SERVICE_URL = process.env.MOVIES_SERVICE_URL;
const EVENTS_SERVICE_URL = process.env.EVENTS_SERVICE_URL;

const GRADUAL_MIGRATION = process.env.GRADUAL_MIGRATION === "true";
const MIGRATION_PERCENT = Number(process.env.MIGRATION_PERCENT || 0);

app.use(express.raw({ type: "*/*" }));

app.get("/health", (req, res) => {
    res.status(200).json({ status: "OK" });
});

app.use(async (req, res) => {
    const urlPath = req.path;
    let targetUrl = MONOLITH_URL;

    if (urlPath.startsWith("/api/movies")) {
        if (
            GRADUAL_MIGRATION &&
            Math.floor(Math.random() * 100) + 1 <= MIGRATION_PERCENT
        ) {
            targetUrl = MOVIES_SERVICE_URL;
            console.log("[Proxy] Routing to MOVIES-SERVICE (Migration Active)");
        } else {
            console.log("[Proxy] Routing to MONOLITH");
        }
    } else if (urlPath.startsWith("/api/events")) {
        targetUrl = EVENTS_SERVICE_URL;
    }

    try {
        const response = await axios.request({
            method: req.method,
            url: `${targetUrl}${urlPath}`,
            params: req.query,
            data: req.body,
            headers: {
                ...req.headers,
                host: undefined
            },
            timeout: 10_000,
            validateStatus: () => true
        });

        const hopByHopHeaders = [
            "connection",
            "keep-alive",
            "proxy-authenticate",
            "proxy-authorization",
            "te",
            "trailer",
            "transfer-encoding",
            "upgrade",
            "content-length"
        ];

        const safeHeaders = { ...response.headers };
        for (const h of hopByHopHeaders) {
            delete safeHeaders[h];
        }
        res
            .status(response.status)
            .set(safeHeaders)
            .send(response.data);

    } catch (err) {
        console.log(err);
        res.status(502).send(`Proxy Error: ${err.message}`);
    }
});

app.listen(port, "0.0.0.0", () => {
    console.log(`Server listening on port ${port}`);
});