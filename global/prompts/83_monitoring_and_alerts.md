# PROMPT 83: MONITORING & ALERTS

**Objective:** Implement a system for monitoring the application's health and performance, and for sending alerts when issues arise.

---

## 🎯 REQUIREMENTS

1.  **Health Checks:** Implement a health check endpoint that returns the status of the application and its dependencies.
2.  **Performance Monitoring:** Monitor key performance indicators (KPIs) such as response time, error rate, and CPU/memory usage.
3.  **Alerting:** Send alerts to a designated channel (e.g., Slack, email) when KPIs cross a certain threshold.
4.  **Dashboard:** Create a dashboard to visualize the application's health and performance.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Health Check
1.  **Create Endpoint:** Create a `/health` endpoint that checks the status of the database, external APIs, and other dependencies.
2.  **Return Status:** The endpoint should return a `200 OK` status if everything is healthy, and a `503 Service Unavailable` status otherwise.

### Phase 2: Performance Monitoring
1.  **Integrate APM:** Integrate an Application Performance Monitoring (APM) tool (e.g., New Relic, Datadog) into the application.
2.  **Configure Monitoring:** Configure the APM tool to monitor the desired KPIs.

### Phase 3: Alerting
1.  **Configure Alerts:** Configure the APM tool to send alerts when KPIs cross a certain threshold.
2.  **Set Up Channels:** Set up the desired alerting channels (e.g., a Slack webhook).

### Phase 4: Dashboard
1.  **Create Dashboard:** Create a dashboard in the APM tool to visualize the application's health and performance.
2.  **Add Widgets:** Add widgets to the dashboard to display the most important KPIs.

---

## ✅ SUCCESS CRITERIA

- The application has a health check endpoint.
- The application's performance is monitored.
- Alerts are sent when issues arise.
- There is a dashboard to visualize the application's health and performance.
