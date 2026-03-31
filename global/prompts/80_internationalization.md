# PROMPT 80: INTERNATIONALIZATION (I18N)

**Objective:** Prepare the application for localization by externalizing all user-facing strings.

---

## 🎯 REQUIREMENTS

1.  **Externalize Strings:** All user-facing strings must be moved out of the code and into a separate resource file (e.g., a JSON file).
2.  **Key-Based System:** Use a key-based system to reference strings (e.g., `t("header.title")`).
3.  **Pluralization:** The system must support pluralization (e.g., "1 item" vs. "2 items").
4.  **Date/Time Formatting:** Use a library to format dates, times, and numbers according to the user's locale.
5.  **Directionality:** The application must support both left-to-right (LTR) and right-to-left (RTL) languages.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Setup
1.  **Install Library:** Add an i18n library (e.g., i18next, react-i18next) to the project.
2.  **Create Resource Files:** Create resource files for each supported language (e.g., `en.json`, `es.json`).
3.  **Configure Library:** Configure the i18n library to load the correct resource file based on the user's language.

### Phase 2: Externalization
1.  **Extract Strings:** Go through the entire codebase and extract all user-facing strings into the resource files.
2.  **Replace Strings:** Replace the hardcoded strings with calls to the i18n library.

### Phase 3: Formatting & Directionality
1.  **Implement Formatting:** Use the i18n library or a dedicated date/time library to format all dates, times, and numbers.
2.  **Implement Directionality:** Add support for RTL languages by using CSS logical properties (e.g., `margin-inline-start` instead of `margin-left`).

### Phase 4: Verification
1.  **Test All Languages:** Test the application in all supported languages to ensure that all strings are translated correctly.
2.  **Test RTL:** Test the application in an RTL language to ensure that the layout is correct.

---

## ✅ SUCCESS CRITERIA

- No user-facing strings are hardcoded in the application.
- The application supports multiple languages.
- The application supports both LTR and RTL languages.
- Dates, times, and numbers are formatted correctly for each language.
