# Diff Details

Date : 2025-09-03 16:50:52

Directory e:\\KPI_HOSTING - V2.1

Total : 81 files,  147770 codes, -47 comments, 297 blanks, all 148020 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [agents/\_\_init\_\_.py](/agents/__init__.py) | Python | 10 | 0 | 2 | 12 |
| [agents/agent\_manager.py](/agents/agent_manager.py) | Python | 56 | 21 | 19 | 96 |
| [agents/checkmk\_collector.py](/agents/checkmk_collector.py) | Python | 24 | 1 | 10 | 35 |
| [agents/cortex\_collector.py](/agents/cortex_collector.py) | Python | 37 | 17 | 8 | 62 |
| [agents/glpi\_collector.py](/agents/glpi_collector.py) | Python | 24 | 1 | 10 | 35 |
| [agents/rapid7\_collector.py](/agents/rapid7_collector.py) | Python | 26 | 6 | 9 | 41 |
| [analyzers/\_\_init\_\_.py](/analyzers/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [analyzers/vcenter\_analyser.py](/analyzers/vcenter_analyser.py) | Python | 98 | 8 | 19 | 125 |
| [api/\_\_init\_\_.py](/api/__init__.py) | Python | -14 | 0 | -2 | -16 |
| [api/api\_dispatcher.py](/api/api_dispatcher.py) | Python | -20 | -10 | -7 | -37 |
| [api/api\_processor.py](/api/api_processor.py) | Python | -48 | -16 | -13 | -77 |
| [api/checkmk.py](/api/checkmk.py) | Python | -50 | -47 | -13 | -110 |
| [api/cortex.py](/api/cortex.py) | Python | -37 | -17 | -8 | -62 |
| [api/facade.py](/api/facade.py) | Python | -3 | 0 | -3 | -6 |
| [api/glpi.py](/api/glpi.py) | Python | -51 | -23 | -6 | -80 |
| [api/rapid7.py](/api/rapid7.py) | Python | -42 | -16 | -9 | -67 |
| [collectors/azure\_collector.py](/collectors/azure_collector.py) | Python | 36 | 4 | 7 | 47 |
| [collectors/csv\_vcenter\_collector.py](/collectors/csv_vcenter_collector.py) | Python | 24 | 13 | 8 | 45 |
| [collectors/inventory\_manager.py](/collectors/inventory_manager.py) | Python | 40 | 5 | 23 | 68 |
| [collectors/vcenter\_collector.py](/collectors/vcenter_collector.py) | Python | -18 | -58 | 0 | -76 |
| [config/config.yaml](/config/config.yaml) | YAML | 3 | -6 | -3 | -6 |
| [config/exceptions\_oxya.csv](/config/exceptions_oxya.csv) | CSV | 14 | 0 | 0 | 14 |
| [config/ngdt\_portgroups.csv](/config/ngdt_portgroups.csv) | CSV | 348 | 0 | 0 | 348 |
| [config/normalization\_maps.yaml](/config/normalization_maps.yaml) | YAML | 45 | 0 | 5 | 50 |
| [config/oxya\_portgroups.csv](/config/oxya_portgroups.csv) | CSV | 52 | 0 | 1 | 53 |
| [config/settings.py](/config/settings.py) | Python | 41 | -6 | 12 | 47 |
| [connectors/azure\_connector.py](/connectors/azure_connector.py) | Python | 211 | 5 | 30 | 246 |
| [connectors/checkmk\_connector.py](/connectors/checkmk_connector.py) | Python | 34 | 1 | 12 | 47 |
| [connectors/csv\_vcenter\_connector.py](/connectors/csv_vcenter_connector.py) | Python | 25 | 0 | 2 | 27 |
| [connectors/glpi\_connector.py](/connectors/glpi_connector.py) | Python | 56 | 2 | 8 | 66 |
| [connectors/rapid7\_connector.py](/connectors/rapid7_connector.py) | Python | 44 | 11 | 7 | 62 |
| [connectors/sql\_connector.py](/connectors/sql_connector.py) | Python | 1 | 0 | 2 | 3 |
| [connectors/vcenter\_connector.py](/connectors/vcenter_connector.py) | Python | 10 | -28 | -8 | -26 |
| [db/\_\_init\_\_.py](/db/__init__.py) | Python | 1 | 0 | -1 | 0 |
| [db/connection\_pool.py](/db/connection_pool.py) | Python | -41 | -10 | -9 | -60 |
| [db/db\_connector.py](/db/db_connector.py) | Python | 320 | 93 | 63 | 476 |
| [db/db\_model.py](/db/db_model.py) | Python | 205 | 10 | 81 | 296 |
| [exports/AZURE\_VCSI.json](/exports/AZURE_VCSI.json) | JSON | 10,802 | 0 | 0 | 10,802 |
| [exports/AZURE\_VCSI\_ressource\_groups.json](/exports/AZURE_VCSI_ressource_groups.json) | JSON | 23,303 | 0 | 0 | 23,303 |
| [exports/AZURE\_VCSI\_subnets.json](/exports/AZURE_VCSI_subnets.json) | JSON | 5,708 | 0 | 0 | 5,708 |
| [exports/CHECKMK - OXYA-T0.json](/exports/CHECKMK%20-%20OXYA-T0.json) | JSON | 250 | 0 | 0 | 250 |
| [exports/CHECKMK - VIC-T0.json](/exports/CHECKMK%20-%20VIC-T0.json) | JSON | 738 | 0 | 0 | 738 |
| [exports/CHECKMK - VIC-T1.json](/exports/CHECKMK%20-%20VIC-T1.json) | JSON | 7,666 | 0 | 0 | 7,666 |
| [exports/GLPI - GLPI-VCSI.json](/exports/GLPI%20-%20GLPI-VCSI.json) | JSON | 9,653 | 0 | 0 | 9,653 |
| [exports/T0\_NGDT.json](/exports/T0_NGDT.json) | JSON | 1,484 | 0 | 0 | 1,484 |
| [exports/VCENTER\_NGDT\_02.json](/exports/VCENTER_NGDT_02.json) | JSON | 1,072 | 0 | 0 | 1,072 |
| [exports/VCENTER\_NGDT\_03.json](/exports/VCENTER_NGDT_03.json) | JSON | 22,597 | 0 | 0 | 22,597 |
| [exports/VCENTER\_OXYA.json](/exports/VCENTER_OXYA.json) | JSON | 3,423 | 0 | 0 | 3,423 |
| [exports/all\_agents.json](/exports/all_agents.json) | JSON | 18,313 | 0 | 0 | 18,313 |
| [exports/all\_inventory.json](/exports/all_inventory.json) | JSON | 39,380 | 0 | 0 | 39,380 |
| [imports/rvtools\_T0.csv](/imports/rvtools_T0.csv) | CSV | 93 | 0 | 1 | 94 |
| [logs/03-09-2025\_14-34-04\_main\_app.log](/logs/03-09-2025_14-34-04_main_app.log) | Log | 81 | 0 | 1 | 82 |
| [logs/03-09-2025\_14-43-21\_main\_app.log](/logs/03-09-2025_14-43-21_main_app.log) | Log | 141 | 0 | 1 | 142 |
| [logs/03-09-2025\_14-47-42\_main\_app.log](/logs/03-09-2025_14-47-42_main_app.log) | Log | 82 | 0 | 1 | 83 |
| [logs/03-09-2025\_15-42-42\_main\_app.log](/logs/03-09-2025_15-42-42_main_app.log) | Log | 24 | 0 | 1 | 25 |
| [logs/03-09-2025\_15-45-54\_main\_app.log](/logs/03-09-2025_15-45-54_main_app.log) | Log | 29 | 0 | 1 | 30 |
| [logs/03-09-2025\_15-46-40\_main\_app.log](/logs/03-09-2025_15-46-40_main_app.log) | Log | 29 | 0 | 1 | 30 |
| [logs/03-09-2025\_15-46-57\_main\_app.log](/logs/03-09-2025_15-46-57_main_app.log) | Log | 29 | 0 | 1 | 30 |
| [logs/03-09-2025\_15-54-55\_main\_app.log](/logs/03-09-2025_15-54-55_main_app.log) | Log | 30 | 0 | 1 | 31 |
| [logs/03-09-2025\_15-56-14\_main\_app.log](/logs/03-09-2025_15-56-14_main_app.log) | Log | 31 | 0 | 1 | 32 |
| [logs/03-09-2025\_15-58-29\_main\_app.log](/logs/03-09-2025_15-58-29_main_app.log) | Log | 32 | 0 | 1 | 33 |
| [logs/03-09-2025\_15-59-19\_main\_app.log](/logs/03-09-2025_15-59-19_main_app.log) | Log | 32 | 0 | 1 | 33 |
| [logs/03-09-2025\_15-59-55\_main\_app.log](/logs/03-09-2025_15-59-55_main_app.log) | Log | 33 | 0 | 1 | 34 |
| [logs/03-09-2025\_16-00-26\_main\_app.log](/logs/03-09-2025_16-00-26_main_app.log) | Log | 1,066 | 0 | 1 | 1,067 |
| [logs/03-09-2025\_16-01-41\_main\_app.log](/logs/03-09-2025_16-01-41_main_app.log) | Log | 25 | 0 | 1 | 26 |
| [logs/03-09-2025\_16-04-23\_main\_app.log](/logs/03-09-2025_16-04-23_main_app.log) | Log | 25 | 0 | 1 | 26 |
| [logs/03-09-2025\_16-44-29\_main\_app.log](/logs/03-09-2025_16-44-29_main_app.log) | Log | 26 | 0 | 1 | 27 |
| [logs/03-09-2025\_16-45-51\_main\_app.log](/logs/03-09-2025_16-45-51_main_app.log) | Log | 29 | 0 | 1 | 30 |
| [logs/03-09-2025\_16-46-20\_main\_app.log](/logs/03-09-2025_16-46-20_main_app.log) | Log | 29 | 0 | 1 | 30 |
| [logs/12-08-2025\_11-57-27\_main\_app.log](/logs/12-08-2025_11-57-27_main_app.log) | Log | -11 | 0 | -1 | -12 |
| [logs/12-08-2025\_14-26-59\_main\_app.log](/logs/12-08-2025_14-26-59_main_app.log) | Log | -4 | 0 | -1 | -5 |
| [logs/12-08-2025\_14-27-53\_main\_app.log](/logs/12-08-2025_14-27-53_main_app.log) | Log | -4 | 0 | -1 | -5 |
| [logs/12-08-2025\_14-29-10\_main\_app.log](/logs/12-08-2025_14-29-10_main_app.log) | Log | -4 | 0 | -1 | -5 |
| [main.py](/main.py) | Python | -17 | 0 | -6 | -23 |
| [utils/data\_normalizer.py](/utils/data_normalizer.py) | Python | 6 | 19 | 8 | 33 |
| [utils/normalization\_strategies.py](/utils/normalization_strategies.py) | Python | 62 | -19 | 13 | 56 |
| [workers/\_\_init\_\_.py](/workers/__init__.py) | Python | -2 | 0 | 0 | -2 |
| [workers/api\_worker.py](/workers/api_worker.py) | Python | -46 | -46 | -10 | -102 |
| [workers/server\_agents\_worker.py](/workers/server_agents_worker.py) | Python | 31 | 21 | 10 | 62 |
| [workers/server\_db\_worker.py](/workers/server_db_worker.py) | Python | 28 | 18 | 6 | 52 |
| [workers/server\_worker.py](/workers/server_worker.py) | Python | 15 | -1 | 4 | 18 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details