import json
import random
import hashlib
from pathlib import Path

# Configurações
POOL_SIZE = 30000
COUNTRIES = [
    {"code": "USA", "tax_name": "SSN", "format": "000-00-0000"},
    {"code": "PRT", "tax_name": "NIF", "format": "000000000"},
    {"code": "ESP", "tax_name": "NIE", "format": "X0000000X"},
    {"code": "GBR", "tax_name": "NI", "format": "XX 00 00 00 X"},
    {"code": "FRA", "tax_name": "NIR", "format": "0 00 00 00 000 000"},
    {"code": "ITA", "tax_name": "Codice Fiscale", "format": "XXXXXX00X00X000X"},
    {"code": "DEU", "tax_name": "Steuer-ID", "format": "00 000 000 000"},
    {"code": "CAN", "tax_name": "SIN", "format": "000-000-000"},
    {"code": "MEX", "tax_name": "RFC", "format": "XXXX000000XXX"},
    {"code": "JPN", "tax_name": "My Number", "format": "0000-0000-0000"},
    {"code": "CHN", "tax_name": "Resident ID", "format": "00000000000000000X"},
    {"code": "AUS", "tax_name": "TFN", "format": "000 000 000"},
    {"code": "IND", "tax_name": "PAN", "format": "XXXXX0000X"},
    {"code": "ARE", "tax_name": "Emirates ID", "format": "784-0000-0000000-0"},
    {"code": "BRA", "tax_name": "CPF/CNPJ", "format": "000.000.000-00"},
    {"code": "ARG", "tax_name": "CUIT", "format": "00-00000000-0"},
    {"code": "CHL", "tax_name": "RUT", "format": "00.000.000-X"},
    {"code": "COL", "tax_name": "NIT", "format": "000.000.000-0"},
    {"code": "PER", "tax_name": "RUC", "format": "00000000000"},
    {"code": "CHE", "tax_name": "AHV", "format": "756.0000.0000.00"},
    {"code": "IRL", "tax_name": "PPS", "format": "0000000XX"},
    {"code": "NLD", "tax_name": "BSN", "format": "0000.00.000"},
    {"code": "SWE", "tax_name": "Personal ID", "format": "000000-0000"},
    {"code": "NOR", "tax_name": "Birth No", "format": "000000 00000"},
    {"code": "DNK", "tax_name": "CPR", "format": "000000-0000"},
    {"code": "ZAF", "tax_name": "ID", "format": "000000 0000 00 0"},
    {"code": "ISR", "tax_name": "ID", "format": "000000000"},
    {"code": "SGP", "tax_name": "NRIC", "format": "X0000000X"},
    {"code": "KOR", "tax_name": "Resident ID", "format": "000000-0000000"},
    {"code": "NZL", "tax_name": "IRD", "format": "00-000-000"}
]

NAMES = ["Liam", "Noah", "Oliver", "James", "Elijah", "William", "Henry", "Lucas", "Benjamin", "Theodore", "Mateo", "Levi", "Sebastian", "Daniel", "Jack", "Emma", "Olivia", "Amelia", "Sophia", "Charlotte", "Ava", "Isabella", "Mia", "Luna", "Evelyn", "Gianna", "Lily", "Aria", "Aurora", "Ellie"]
SURNAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzales", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]
STREETS = ["Broadway", "Maple St", "Oak Ave", "Sunset Blvd", "Park Ln", "River Rd", "Main St", "Cedar Dr", "Pine St", "Washington Ave"]
BANKS = ["Chase Bank", "Bank of America", "HSBC", "Santander", "Barclays", "BNP Paribas", "Deutsche Bank", "Wells Fargo", "Itaú Unibanco", "Banco do Brasil", "Scotiabank", "MUFG", "ICBC", "Standard Chartered"]
PURPOSES = ["Family Support", "Real Estate Investment", "Professional Services", "Education Fees", "Medical Expenses", "Savings Transfer", "Tourism/Travel", "Trade Settlement", "Freelancer Payout"]
SECTORS = ["Agribusiness", "Technology/SaaS", "General Commerce", "Import/Export", "Logistics", "Energy", "Financial Services", "Healthcare", "Manufacturing"]

def gen_random_by_format(fmt, rng):
    res = ""
    for c in fmt:
        if c == '0': res += str(rng.randint(0, 9))
        elif c == 'X': res += chr(rng.randint(65, 90))
        else: res += c
    return res

def generate_pool():
    rng = random.Random(42) # Determinístico
    pool = []
    
    for i in range(1, POOL_SIZE + 1):
        country = rng.choice(COUNTRIES)
        is_pj = rng.random() < 0.15 # 15% PJ
        
        raw_name = rng.choice(NAMES) + " " + rng.choice(SURNAMES)
        if is_pj:
            raw_name += " " + rng.choice(["LTDA", "S/A", "Holdings", "Corp", "LLC"])
        
        entity_id = f"ENT-{i:05d}"
        tax_id = gen_random_by_format(country["format"], rng)
        if country["code"] == "BRA":
             # Ajuste CPF/CNPJ
             if is_pj: tax_id = gen_random_by_format("00.000.000/0001-00", rng)
             else: tax_id = gen_random_by_format("000.000.000-00", rng)

        profile = {
            "entity_id": entity_id,
            "type": "PJ" if is_pj else "PF",
            "name": raw_name,
            "dob": f"{rng.randint(1960, 2005)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            "gender": rng.choice(["M", "F", "O"]),
            "country": country["code"],
            "tax_id": tax_id,
            "tax_name": country["tax_name"],
            "email": f"{raw_name.lower().replace(' ', '.')}@example.com",
            "phone": f"+{rng.randint(1, 999)} {rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}",
            "address": f"{rng.randint(10, 9999)} {rng.choice(STREETS)}, {rng.choice(SURNAMES)} City",
            "bank_name": rng.choice(BANKS),
            "bank_acc": gen_random_by_format("XXXXXXXXXXXX", rng) if country["code"] in ["USA", "JPN"] else gen_random_by_format("PT00 0000 0000 0000 0000 0000", rng),
            "card_bin": str(rng.randint(400000, 599999)),
            "sector": rng.choice(SECTORS) if is_pj else "Personal",
            "risk_score": rng.randint(0, 100)
        }
        pool.append(profile)
        
    out = Path("c:/LAPTOP/remitly-p2p/06_DATA/KYC_MASTER_POOL_30K.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pool, indent=2), encoding="utf-8")
    print(f"Pool de {POOL_SIZE} entidades gerado em {out}")

if __name__ == "__main__":
    generate_pool()
