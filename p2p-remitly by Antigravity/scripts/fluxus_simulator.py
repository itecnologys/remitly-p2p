import math

class FluxusSimulator:
    def __init__(self, initial_users=1000, growth_rate=0.15, avg_remittance=500, tx_per_month=1.2):
        # Operational Parameters (Institutional Standard)
        self.initial_users = initial_users
        self.growth_rate = growth_rate  # 15% WoW or MoM? Let's assume MoM for initial 60 months
        self.avg_remittance = avg_remittance # USD
        self.tx_per_month = tx_per_month
        
        # Spread Configuration (Success Book V-2 Logic)
        self.platform_fee_rate = 0.010 # 1.0%
        self.investor_yield_rate = 0.015 # 1.5%
        self.vasp_fee_rate = 0.010 # 1.0%
        
        # OPEX - API Costs (Blueprint Engine Logic)
        self.cost_id_verification = 1.35 # SumSub initial
        self.cost_aml_monitoring = 0.20 # SumSub monthly/user
        self.cost_virtual_card = 0.10 # Stripe/Marqeta
        self.cost_physical_card_issuing = 3.50 # Stripe/Marqeta
        self.cost_gas_polygon = 0.01 # Average Gas
        
        # Infrastructure (Monthly Fixed)
        self.fixed_infra_cost = 2500 # Fireblocks, AWS, Support
        
        # Card Usage Logic
        self.card_penetration_rate = 0.60 # 60% of users use card
        self.avg_card_monthly_spend = 300 # USD
        self.interchange_revenue_rate = 0.005 # 0.5% net margin from card
        
    def simulate(self, months=12, output_file=None):
        results = []
        current_users = self.initial_users
        total_gtv = 0
        total_profit = 0
        total_revenue = 0
        
        header = f"{'Month':<6} | {'Users':<10} | {'GTV (USD)':<15} | {'Revenue':<15} | {'OPEX':<12} | {'Net Profit':<12} | {'EBITDA':<8}"
        separator = "-" * 90
        
        print(header)
        print(separator)
        if output_file:
            output_file.write(header + "\n")
            output_file.write(separator + "\n")
        
        for m in range(1, months + 1):
            new_users = current_users * self.growth_rate if m > 1 else 0
            current_users += new_users
            
            # Remittance Volume (GTV)
            monthly_gtv = current_users * self.tx_per_month * self.avg_remittance
            
            # Revenues
            remittance_revenue = monthly_gtv * self.platform_fee_rate
            card_usage_revenue = (current_users * self.card_penetration_rate) * self.avg_card_monthly_spend * self.interchange_revenue_rate
            total_monthly_revenue = remittance_revenue + card_usage_revenue
            
            # Costs (OPEX)
            onboarding_costs = new_users * self.cost_id_verification
            maintenance_costs = current_users * self.cost_aml_monitoring
            tx_costs = (current_users * self.tx_per_month) * self.cost_gas_polygon
            card_opex = (new_users * self.card_penetration_rate) * self.cost_virtual_card
            
            monthly_opex = onboarding_costs + maintenance_costs + tx_costs + card_opex + self.fixed_infra_cost
            
            monthly_net = total_monthly_revenue - monthly_opex
            ebitda_margin = (monthly_net / total_monthly_revenue) * 100 if total_monthly_revenue > 0 else 0
            
            total_gtv += monthly_gtv
            total_profit += monthly_net
            total_revenue += total_monthly_revenue
            
            row = f"{m:<6} | {int(current_users):<10,} | {monthly_gtv:15,.2f} | {total_monthly_revenue:15,.2f} | {monthly_opex:12,.2f} | {monthly_net:12,.2f} | {ebitda_margin:7.1f}%"
            print(row)
            if output_file:
                output_file.write(row + "\n")
            
        summary = (
            f"{separator}\n"
            f"RESUMO EXECUTIVO ({months} MESES)\n"
            f"{separator}\n"
            f"GTV ACUMULADO:   ${total_gtv:15,.2f}\n"
            f"RECEITA BRUTA:   ${total_revenue:15,.2f}\n"
            f"LUCRO LÍQUIDO:   ${total_profit:15,.2f}\n"
            f"MARGEM MÉDIA:    {(total_profit/total_revenue)*100:15.2f}%\n"
            f"{separator}\n"
        )
        print(summary)
        if output_file:
            output_file.write(summary + "\n")
        
if __name__ == "__main__":
    simulator = FluxusSimulator()
    RESULT_PATH = r'c:\LAPTOP\remitly-p2p\p2p-remitly by Antigravity\FLUXUS_DRE_SIMULATION.txt'
    
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        f.write("FLUXUS DRE SIMULATION REPORT - INSTITUTIONAL GRADE\n")
        f.write("Currency: USD\n\n")
        
        print("\n--- PROJEÇÃO OPERACIONAL (12 MESES) ---")
        f.write("--- PROJEÇÃO OPERACIONAL (12 MESES) ---\n")
        simulator.simulate(12, output_file=f)
        
        print("\n--- PROJEÇÃO INSTITUCIONAL / SÉRIE-A (60 MESES) ---")
        f.write("\n--- PROJEÇÃO INSTITUCIONAL / SÉRIE-A (60 MESES) ---\n")
        simulator.simulate(60, output_file=f)
    
    print(f"Relatório salvo em: {RESULT_PATH}")
