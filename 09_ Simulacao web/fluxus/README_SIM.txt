FLUXUS — simulação web (HTML + SQLite local)

1) Regenerar base (após mudar o CSV oficial):
   python ..\..\05_SCRIPTS\SCRIPT_BUILD_FLUXUS_SIM_DB.py
   Se fluxus_sim.db estiver aberto no servidor, o script grava fluxus_sim_ready.db;
   o server_sim.py usa automaticamente o ficheiro mais recente.

2) Subir servidor (API + ficheiros estáticos):
   pip install flask
   python server_sim.py

3) Abrir no browser:
   http://127.0.0.1:8787/
   http://127.0.0.1:8787/transaction.html  (rematches DRE + visões por LP / resumo)
   http://127.0.0.1:8787/stress-audit.html  (log Power BI: executivo, por mês, por LP, ledger)

4) Regenerar base stress (DATA_STRESS_TEST_AUDIT_LOG_POWERBI.csv):
   python ..\..\05_SCRIPTS\SCRIPT_BUILD_STRESS_AUDIT_DB.py
   Gera fluxus/data/fluxus_stress.db consumido por /api/stress/*

Nota: abrir os HTML em file:// não carrega os 84k rematches (API inacessível).
