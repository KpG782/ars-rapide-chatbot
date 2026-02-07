# ARS Rapide — Dataset Sources & How to Extend Them

**Every file in your `knowledge_base/` folder has a source. This document is your paper trail.**

Judges will ask where your data came from. This is your answer. Every dataset here is either open source, publicly available, or compiled from public information with clear attribution.

---

## 1. car_problems.json

**What it contains:** 25 car problems with symptoms, diagnoses, urgency levels, OBD-II DTC codes, and Taglish symptom variants.

**Primary sources:**

**Zenodo — Automotive Faults Dataset** (CC BY 4.0 — you can use it)
- URL: https://zenodo.org/records/15626055
- File: `automotive_faults_aktc_obike_et_al.json`
- What to take from it: The structured fault-symptom-diagnosis mappings. The JSON structure includes symptoms, diagnostic procedures, and resolution outcomes. Download it, study the format, and use it as your baseline. Our `car_problems.json` mirrors this structure but is adapted for PH vehicles and pricing.
- Citation: Obike, Peter. 2024. "Automotive Faults Dataset for Diagnostic and Maintenance Systems." Zenodo. DOI: 10.5281/zenodo.15626055

**OBD-II DTC Code Databases** (for the `dtc_codes` field)
- GitHub: https://github.com/mytrile/obd-trouble-codes — OBD trouble codes in JSON, CSV, and SQLite. Download the CSV and cross-reference the codes in your `car_problems.json`.
- GitHub: https://github.com/todrobbins/dtcdb — Open data collection of OBD-II PIDs and DTCs.
- GitHub Gist: https://gist.github.com/wzr1337/8af2731a5ffa98f9d506537279da7a0e — Complete DTC mapping in JSON. This is a single file you can download and parse.
- Community: https://obdb.community — OBDb is the open source community effort to document all OBD diagnostic codes. Organized by vehicle make and model.

**How to extend it:**
1. Download the Zenodo JSON file.
2. Download the DTC mapping gist.
3. For each new car problem you want to add, look up the relevant DTC codes from the gist.
4. Add Taglish symptoms by checking the `taglish_terms.json` file and the Tsikot forums (see below).
5. Map it to PH-popular vehicles (see vehicles list below).

---

## 2. pricing.json

**What it contains:** Metro Manila 2024-2025 auto repair pricing in PHP, split into talyer (local shop) and casa (dealership) tiers.

**Sources (all publicly available Philippine pricing data):**

- Moneymax — "10 Auto Repair Shop Options" — https://www.moneymax.ph/car-insurance/articles/auto-repair-shop-service-centers — Lists average costs for common Metro Manila auto services.
- MoneySmart PH — "How to Save Money with Auto Servicing" — https://www.moneysmart.ph/articles/how-to-save-money-with-auto-servicing-in-the-philippines — States PMS costs range from ₱2,500 (local) to ₱25,000 (casa). Lists estimated PMS costs for popular passenger cars.
- Moneymax — "Cost of Owning a Car in the Philippines" — https://www.moneymax.ph/car-insurance/articles/expenses-cars — Average annual repair cost ₱14,000, PMS at 10k-20k km is ₱3,600-5,700.
- Tsikot Forums — https://www.tsikot.com/forums/ — Real Filipino mechanics and car owners sharing actual repair quotes. Search for specific repairs to get current pricing.

**How to extend it:**
1. Go to Tsikot.com and search for the service you want to price (e.g., "clutch replacement cost Philippines").
2. Look at what real people paid. Take the range.
3. Cross-reference with one dealership quote (call a Toyota or Honda casa, get an actual quote).
4. Add both prices to your JSON under `talyer_price_php` and `casa_price_php`.
5. Update prices quarterly — PH inflation affects parts costs.

---

## 3. taglish_terms.json

**What it contains:** Filipino-English automotive vocabulary — car parts, common problem descriptions in Taglish, mechanic conversation phrases, and urgency expressions.

**Sources:**

- Talkpal — "Automotive and Mechanical Terms in Tagalog" — https://talkpal.ai/vocabulary/automotive-and-mechanical-terms-in-tagalog/ — Comprehensive Tagalog automotive glossary with example sentences.
- ProZ KudoZ — Filipino Automotive Terms Translation — https://www.proz.com/kudoz/english-to-tagalog/tech-engineering/91644-automotive-terms-2.html — Professional translators providing Filipino mechanic terms. Includes terms like "tambutso" (muffler), "langis pangmakina" (engine oil), "grasa" (grease).
- Tsikot.com Forums — Real Filipino car owners describing problems in Taglish. Search the forums for common car issues to pick up natural Taglish phrasing.

**How to extend it:**
1. Go to Tsikot.com and read how real Filipinos describe car problems.
2. Pick up the natural Taglish phrases they use.
3. Add them to the `car_problems_taglish` section.
4. If you find new car parts or mechanic terms, add them to `car_parts`.
5. This is the one file you should keep updating continuously — the more Taglish you capture, the better your chatbot handles Filipino users.

---

## 4. services.json

**What it contains:** 12 service categories ARS offers, with descriptions, related problems, and included checks.

**Source:** Compiled from standard auto repair service categories used by Philippine dealerships and service centers. Cross-referenced with:
- Toyota Motor Philippines service offerings
- Honda Cars Philippines maintenance schedule — https://www.hondaphil.com/maintenance/maintenance-schedule
- Rapidé Auto Service Center offerings (one of the largest chains in PH with 50+ branches)

**How to extend it:** Add new service categories as ARS expands. Each service should map to at least one problem in `car_problems.json` via the `related_problems` field.

---

## Philippine Vehicle Reference (for car_problems.json)

**Top 10 best-selling cars in the Philippines 2024** (from AutoIndustriya.com — https://www.autoindustriya.com/auto-industry-news/10-best-selling-cars-of-2024-in-the-philippines.html):

| Rank | Model | Units Sold 2024 | Why it matters for ARS |
|------|-------|----------------|------------------------|
| 1 | Toyota Vios | 43,636 | Most common car in PH. Must have excellent coverage. |
| 2 | Toyota Hilux | 26,643 | Top pickup. Heavy use, high wear. |
| 3 | Mitsubishi Mirage G4 | ~26,000 | Budget car. Common transmission issues. |
| 4 | Mitsubishi Xpander | 26,242 | Family MPV. AC issues common in PH heat. |
| 5 | Toyota Wigo | ~22,000 | Entry-level. Simple maintenance. |
| 6 | Toyota Raize | ~20,000 | Compact SUV. Growing fast. |
| 7 | Toyota Innova | 17,648 | Workhorse MPV. Diesel and gasoline variants. |
| 8 | Toyota Avanza | 17,489 | Budget MPV. |
| 9 | Toyota HiAce | 15,744 | Commercial van. Heavy use. |
| 10 | Mitsubishi L300 | 13,939 | Commercial van. Very high mileage. |

**Source:** Manila Bulletin / AutoIndustriya 2024 sales data. Toyota dominated with 45.4% market share. Mitsubishi second at 18.8%.

**How to use this:** When adding new problems to `car_problems.json`, fill in the `common_ph_vehicles` field with models from this list. Prioritize Toyota and Mitsubishi — they cover 60%+ of the PH market.

---

## GitHub Repositories for OBD-II & Vehicle Data

These are additional open-source repos you can pull data from as the project grows:

| Repo | URL | What's useful |
|------|-----|---------------|
| us-car-models-data | https://github.com/abhionlyone/us-car-models-data | 15,000+ car models with specs. Useful for the car details form. |
| obd-trouble-codes | https://github.com/mytrile/obd-trouble-codes | DTC codes in CSV, JSON, and SQLite. Pull all generic P-codes. |
| dtcdb | https://github.com/todrobbins/dtcdb | OBD-II PID database. |
| OBDb (community) | https://github.com/OBDb | Vehicle-specific OBD data organized by make/model. CC BY-SA licensed. |
| Automotive_Diagnostics | https://github.com/hayatu4islam/Automotive_Diagnostics | OBD-II sensor data analysis. Good for understanding what the sensor values mean. |

---

## How to cite this in your competition submission

If judges ask about data provenance, here is your statement:

> "The ARS knowledge base is compiled from open-source automotive fault datasets (Zenodo, CC BY 4.0), community-maintained OBD-II diagnostic code databases (GitHub, CC BY-SA), and publicly available Philippine automotive pricing and terminology data from established local sources including Tsikot.com, Moneymax, and AutoIndustriya. All vehicle-specific data is mapped to the top-selling models in the Philippine market based on 2024 CAMPI sales figures."

---

*Last updated: February 2026*
*All sources verified and accessible as of this date.*
